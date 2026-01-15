from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from db.session import get_session
from db.models import VideosOrm, StatusEnum
from schemas.videos import VideoAddForm, VideosGetForm
from typing import Annotated



router = APIRouter(prefix="/videos", tags=['videos'])


@router.post("")
async def add_video(
    data: VideoAddForm,
    session: AsyncSession = Depends(get_session)
):
    video = VideosOrm(**data.__dict__)
    session.add(video)
    await session.commit()
    await session.refresh(video)

    return video.to_dict()


@router.get("")
async def get_videos(
    video_form: Annotated[VideosGetForm, Query()],
    session: AsyncSession = Depends(get_session)
):
    query = select(VideosOrm)

    if video_form.status:
        query = query.where(VideosOrm.status.in_(video_form.status))

    if video_form.camera_number:
        query = query.where(VideosOrm.camera_number.in_(video_form.camera_number))

    if video_form.location:
        query = query.where(VideosOrm.location.in_(video_form.location))

    if video_form.start_time_from:
        query = query.where(VideosOrm.start_time >= video_form.start_time_from)

    if video_form.start_time_to:
        query = query.where(VideosOrm.start_time <= video_form.start_time_to)

    result = await session.execute(query)
    
    return result.scalars().all()


@router.get("/{video_id}")
async def get_video_by_id(
    video_id: int,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(VideosOrm).filter_by(id=video_id)
    res = await session.execute(stmt)
    obj = res.scalar_one_or_none()

    if obj is None:
        raise HTTPException(404)
    
    return obj
    

@router.patch("/{video_id}/status")
async def change_status(
    video_id: int,
    status: StatusEnum,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(VideosOrm).filter_by(id=video_id)
    res = await session.execute(stmt)
    obj = res.scalar_one_or_none()

    if obj is None:
        raise HTTPException(404)
    
    obj.status = status
    await session.commit()
    await session.refresh(obj)

    return obj
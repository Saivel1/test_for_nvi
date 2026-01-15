import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.videos import VideoAddForm, VideosGetForm
from db.models import StatusEnum, VideosOrm
from sqlalchemy import select


@pytest.mark.asyncio
async def test_creation(db_session: AsyncSession):
    from api.videos import add_video

    data = { 
        "video_path": "/storage/camera1/2024-01-15_10-30-00.mp4",  
        "start_time": "2024-01-15T10:30:00", 
        "duration": "PT1H", 
        "camera_number": 1, 
        "location": "Entrance" 
    }

    data_in = VideoAddForm(**data)

    res = await add_video(data=data_in, session=db_session)

    assert res
    assert res['status'] == "new"
    assert res['id'] == 1


@pytest.mark.asyncio
async def test_get_list(
    db_session: AsyncSession,
    video_notes
):
    from api.videos import get_videos

    data_in = VideosGetForm(status=[StatusEnum.NEW, StatusEnum.TRANSCODE, StatusEnum.RECOGNIZED])

    res = await get_videos(video_form=data_in, session=db_session)

    assert res



@pytest.mark.asyncio
async def test_get_by_id(
    db_session: AsyncSession,
    video_note
):
    from api.videos import get_video_by_id

    res = await get_video_by_id(
        video_id=1,
        session=db_session
    )

    assert res


@pytest.mark.asyncio
async def test_change_status(
    db_session: AsyncSession,
    video_note
):
    from api.videos import change_status

    res = await change_status(
        video_id=1,
        status=StatusEnum.RECOGNIZED,
        session=db_session
    )

    assert res

    stmt = select(VideosOrm).filter_by(id=1)
    res = await db_session.execute(stmt)
    obj = res.scalar_one_or_none()

    assert obj is not None
    assert obj.status == StatusEnum.RECOGNIZED
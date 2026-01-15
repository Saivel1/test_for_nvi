from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Interval, func
from datetime import datetime, timedelta
from enum import Enum


class Base(DeclarativeBase):
    pass


class StatusEnum(str, Enum):
    NEW = "new"
    TRANSCODE = "transcoded"
    RECOGNIZED = "recognized"


class VideosOrm(Base):
    __tablename__ = 'vides'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video_path: Mapped[str]
    start_time: Mapped[datetime]
    duration: Mapped[timedelta] = mapped_column(Interval)
    camera_number: Mapped[int]
    location: Mapped[str]
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.NEW)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def to_dict(self):
        """Преобразует объект в словарь"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

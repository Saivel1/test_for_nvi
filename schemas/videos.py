from pydantic import BaseModel, field_validator, Field, ConfigDict
from datetime import datetime, timedelta
from db.models import StatusEnum


class VideoAddForm(BaseModel):
    video_path: str
    start_time: datetime
    duration: timedelta
    camera_number: int = Field(..., gt=0)
    location: str


    @field_validator("video_path")
    @classmethod
    def non_empty_path(cls, v: str):
        if v == "" or not v:
            raise ValueError("video_path Не может быть пустым")
        return v
    

    @field_validator("location")
    @classmethod
    def non_empty_location(cls, v: str):
        if v == "" or not v:
            raise ValueError("video_path Не может быть пустым")
        return v
    

    @field_validator("duration")
    @classmethod
    def positive_duration(cls, v: timedelta):
        if v <= timedelta(0):
            raise ValueError("duration Должен быть положительны интервалом")
        return v
    


class VideosGetForm(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: list[StatusEnum] | None = None
    camera_number: list[int] | None = None
    location: list[str] | None = None
    start_time_from: datetime | None = None
    start_time_to: datetime | None = None
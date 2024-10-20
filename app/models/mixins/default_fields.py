from sqlmodel import SQLModel, Column, Field
from sqlalchemy import DateTime, func
from typing import Optional
import datetime


class TimestampMixin(SQLModel):
    """
    Mixin for timestamp columns
    """

    soft_delete: bool = Field(default=False)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
    updated_at: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )

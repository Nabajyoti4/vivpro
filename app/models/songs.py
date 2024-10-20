from enum import IntEnum
from decimal import Decimal

from sqlmodel import Field, Enum, Column

from app.models.mixins.default_fields import TimestampMixin


class ModeEnum(IntEnum):
    off = 0
    on = 1


class Songs(TimestampMixin, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    playlist_id: str = Field(unique=True, index=True)
    title: str = Field(max_length=250)
    danceability: Decimal = Field(default=0, max_digits=5, decimal_places=3)
    energy: Decimal = Field(default=0, max_digits=5, decimal_places=3)
    mode: ModeEnum = Field(sa_column=Column(Enum(ModeEnum)), default=ModeEnum.on)
    acousticness: Decimal = Field(default=0, max_digits=10, decimal_places=10)
    tempo: Decimal = Field(default=0, max_digits=6, decimal_places=3)
    duration_ms: int = Field()
    num_sections: int = Field()
    num_segments: int = Field()
    rating: int = Field()

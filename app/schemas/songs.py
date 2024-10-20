from typing import Literal, Optional
import decimal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at", "id"] = "created_at"
    order_dir: Literal["asc", "desc"] = "asc"
    search_title: Optional[str] = None


class Songs(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    playlist_id: str
    title: str
    danceability: decimal.Decimal
    energy: decimal.Decimal
    mode: int
    acousticness: decimal.Decimal
    tempo: decimal.Decimal
    duration_ms: int
    num_sections: int
    num_segments: int
    rating: int
    created_at: datetime
    updated_at: Optional[datetime]


class SongsResponse(BaseModel):
    songs: list[Songs]
    total: int


class SongsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    danceability: Optional[decimal.Decimal] = None
    energy: Optional[decimal.Decimal] = None
    mode: Optional[int] = Field(None, ge=0, le=1)
    acousticness: Optional[decimal.Decimal] = None
    tempo: Optional[decimal.Decimal] = None
    duration_ms: Optional[int] = None
    num_sections: Optional[int] = None
    num_segments: Optional[int] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

"""
Songs endpoints for users.
"""

from typing import Annotated

from fastapi import File, UploadFile, APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_async_session
from app.services.songs import SongsService
from app.schemas.songs import FilterParams, SongsUpdate


songs_router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
    responses={404: {"description": "Not found"}},
)


@songs_router.post("/", description="Upload the json file with songs")
async def create_song(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Upload the json file with songs.
    """

    # get file extension
    songs_service = SongsService()
    data_created = await songs_service.create_song(file, session)

    return JSONResponse(content=data_created, status_code=201)


@songs_router.get("/", description="Get all songs")
async def get_songs(
    filter_query: Annotated[FilterParams, Query()],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get all songs.
    """
    songs_service = SongsService()
    songs = await songs_service.get_songs(filter_query, session)

    return JSONResponse(content=songs, status_code=200)


@songs_router.patch("/{song_id}", description="Update the song rating")
async def update_song(
    song_id: int,
    songs_update_data: SongsUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update the song rating.
    """
    songs_service = SongsService()
    updated_song = await songs_service.update_song(song_id, songs_update_data, session)

    return JSONResponse(content=updated_song, status_code=200)

"""
This file contains all the routes for the API.
"""

from fastapi import APIRouter

from app.routes.v1.endpoints import songs
from app.core.config import settings


api_router = APIRouter(
    prefix=settings.API_V1_STR,
)

# Admin Routes
api_router.include_router(songs.songs_router)

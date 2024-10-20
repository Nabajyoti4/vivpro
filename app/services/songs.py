"""
Songs Service
"""

import json

from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.songs import CRUDSongs
from app.schemas.songs import SongsResponse
from app.core.logger_config import api_logger


class SongsService:
    def __init__(self):
        pass

    async def create_song(self, file: UploadFile, session: AsyncSession):
        """
        Create a new song
        """
        try:
            with open(file.filename, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            with open(file.filename, "r") as f:
                json_data = json.load(f)

            rows = []

            # Step 3: Iterate through the keys and map the data
            for index in json_data["id"].keys():
                row = {
                    "playlist_id": json_data["id"].get(index, None),
                    "title": json_data["title"].get(index, None),
                    "danceability": json_data["danceability"].get(index, None),
                    "energy": json_data["energy"].get(index, None),
                    "mode": json_data["mode"].get(index, None),
                    "acousticness": json_data["acousticness"].get(index, None),
                    "tempo": json_data["tempo"].get(index, None),
                    "duration_ms": json_data["duration_ms"].get(index, None),
                    "num_sections": json_data["num_sections"].get(index, None),
                    "num_segments": json_data["num_segments"].get(index, None),
                    "rating": 0,  # Adding default rating for each entry
                }
                rows.append(row)

            song_crud_service = CRUDSongs(session)

            await song_crud_service.store_songs(rows)

            return {
                "message": f"Successfully uploaded {file.filename} file with {len(rows)} rows"
            }
        except Exception as e:
            api_logger.error(f"Error in create_song: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    async def get_songs(self, filter_query, session: AsyncSession):
        """
        Get all songs
        """
        try:
            song_crud_service = CRUDSongs(session)

            db_result = await song_crud_service.get_all_songs(filter_query)

            return jsonable_encoder(
                SongsResponse(songs=db_result["songs"], total=db_result["total_songs"])
            )
        except Exception as e:
            api_logger.error(f"Error in get_songs: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    async def update_song(self, song_id: int, songs_update_data, session: AsyncSession):
        """
        Update the song rating
        """
        try:
            song_crud_service = CRUDSongs(session)

            db_result = await song_crud_service.update_song(song_id, songs_update_data)

            return jsonable_encoder(db_result)
        except Exception as e:
            api_logger.error(f"Error in update_song_rating: {e}")
            raise HTTPException(status_code=400, detail=str(e))

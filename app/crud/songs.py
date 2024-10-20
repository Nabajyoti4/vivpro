"""
CRUD operation for songs
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


from app.models.songs import Songs
from app.core.logger_config import api_logger


class CRUDSongs:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def store_songs(self, bulk_data: list[dict]):
        """
        Create a new song
        """
        try:
            songs_instance = []
            for data in bulk_data:
                song = Songs(**data)
                songs_instance.append(song)

            self.session.add_all(songs_instance)
            await self.session.commit()
            return song
        except Exception as e:
            await self.session.rollback()
            api_logger.error(f"Error in store_songs: {e}")
            raise e

    async def get_all_songs(self, filter_query):
        """
        Get all songs
        """
        try:
            if hasattr(Songs, filter_query.order_by):
                field = getattr(Songs, filter_query.order_by)

                order_by = field if filter_query.order_dir == "asc" else field.desc()

            else:
                raise ValueError(
                    f"Invalid field '{filter_query.order_by}' for ordering."
                )

            statement = select(Songs)

            # Conditionally add the title filter if it exists in the query
            if filter_query.search_title:
                statement = statement.where(
                    Songs.title.ilike(f"%{filter_query.search_title}%")
                )

            total_songs = await self.session.exec(statement)
            total_songs = total_songs.all()

            # Add limit, offset, and order_by
            statement = (
                statement.limit(filter_query.limit)
                .offset(filter_query.offset)
                .order_by(order_by)
            )
            results = await self.session.exec(statement)
            songs = results.all()

            return {
                "songs": songs,
                "total_songs": len(total_songs),
            }
        except Exception as e:
            api_logger.error(f"Error in get_all_songs: {e}")
            raise e

    async def update_song(self, song_id: int, songs_update_data):
        """
        Update the song rating
        """
        try:
            song = await self.session.get(Songs, song_id)
            if not song:
                raise ValueError(f"Song with id {song_id} not found")

            for key, value in songs_update_data.model_dump().items():
                print(key, value)
                if value is not None:
                    setattr(song, key, value)

            self.session.add(song)
            await self.session.commit()
            await self.session.refresh(song)

            return song
        except Exception as e:
            await self.session.rollback()
            api_logger.error(f"Error in update_song: {e}")
            raise e

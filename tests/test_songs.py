"""
This module contains the tests for the songs module.
"""

import pytest
import random
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.main import app


pytestmark = pytest.mark.asyncio


async def test_get_song():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            "api/v1/songs/?limit=10&offset=0&order_by=created_at&order_dir=asc"
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 100


async def test_get_song_by_title():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("api/v1/songs/?search_title=3AM")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["songs"][0]["title"] == "3AM"


async def test_get_song_by_title_empty():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("api/v1/songs/?search_title=jhabjda")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["songs"] == []


async def test_update_song_rating():
    # generate a random rating between 1 and 5

    random_rating = random.randint(1, 5)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.patch("api/v1/songs/208", json={"rating": random_rating})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "3AM"
    assert response.json()["rating"] == random_rating


async def test_update_song_rating_invalid_id():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.patch("api/v1/songs/2080", json={"rating": 5})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Song with id 2080 not found"

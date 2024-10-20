import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from app.main import app


pytestmark = pytest.mark.asyncio


async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health-check")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, world!"}

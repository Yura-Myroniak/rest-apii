import pytest
import pytest_asyncio
import fakeredis.aioredis

from httpx import AsyncClient, ASGITransport

from main import app
import rate_limiter



@pytest_asyncio.fixture(autouse=True)
async def mock_redis():
    fake_redis = fakeredis.aioredis.FakeRedis(
        decode_responses=True
    )

    rate_limiter.r = fake_redis

    yield

    await fake_redis.flushall()


async def get_auth_headers(ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })

    tokens = response.json()

    return {
        "Authorization": f"Bearer {tokens['access_token']}"
    }


@pytest.mark.asyncio
async def test_anonymous_user_under_limit():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.get("/public")

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_anonymous_user_limit_exceeded():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        await ac.get("/public")
        await ac.get("/public")

        response = await ac.get("/public")

        assert response.status_code == 429


@pytest.mark.asyncio
async def test_authenticated_user_under_limit():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        headers = await get_auth_headers(ac)

        response = await ac.get(
            "/books/",
            headers=headers
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_authenticated_user_limit_exceeded():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        headers = await get_auth_headers(ac)

        for _ in range(10):
            await ac.get(
                "/books/",
                headers=headers
            )

        response = await ac.get(
            "/books/",
            headers=headers
        )

        assert response.status_code == 429
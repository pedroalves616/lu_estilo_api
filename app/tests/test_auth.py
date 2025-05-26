import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app



@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "newuser", "email": "newuser@example.com", "password": "password123", "role": "regular"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "regular"
    assert "hashed_password" in data 

@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"username": "dupuser", "email": "dup@example.com", "password": "password123", "role": "regular"}
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "dupuser", "email": "another@example.com", "password": "password123", "role": "regular"}
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"username": "user1", "email": "dupemail@example.com", "password": "password123", "role": "regular"}
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "user2", "email": "dupemail@example.com", "password": "password123", "role": "regular"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, test_user):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, regular_user_token: str):
    response = await client.post(
        "/api/v1/auth/refresh-token",
        headers={"Authorization": f"Bearer {regular_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] != regular_user_token # Should be a new token
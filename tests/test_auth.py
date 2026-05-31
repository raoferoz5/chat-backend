# tests/test_auth.py
import pytest
import time

async def test_home_endpoint(async_client):
    """Test that the home page returns 200 OK."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Chat Backend Running"}

async def test_user_registration(async_client):
    """Test creating a new user with a completely unique payload every run."""
    # Create a dynamic suffix based on the current timestamp
    unique_suffix = int(time.time())
    
    payload = {
        "username": f"user_{unique_suffix}",
        "email": f"email_{unique_suffix}@example.com",
        "password": "securepassword123"
    }
    
    response = await async_client.post("/users/register", json=payload)
    
    # If it still returns a 400, this assertion will display the exact reason why
    assert response.status_code == 201, f"Registration failed: {response.text}"
    assert "id" in response.json()
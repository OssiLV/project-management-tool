import pytest
from app.schemas import UserCreate
from app.crud import create_user
from app.models import User

@pytest.fixture(scope="function")
def test_user(db_session):
    user_data = UserCreate(name="Test User", email="test@example.com", password="testpass", role="member")
    user = create_user(db_session, user_data)
    return user

def test_register(client, db_session):
    response = client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass",
        "role": "member",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "member"
    assert data["is_active"] == 1

def test_login(client, db_session, test_user):
    response = client.post("/token", data={"username": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

def test_get_user(client, db_session, test_user):
    login = client.post("/token", data={"username": "test@example.com", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/users/{test_user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == "test@example.com"

def test_update_user(client, db_session, test_user):
    login = client.post("/token", data={"username": "test@example.com", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.patch(f"/users/{test_user.id}", json={"name": "Updated Name"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_soft_delete_user(client, db_session, test_user):
    login = client.post("/token", data={"username": "test@example.com", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/users/{test_user.id}/soft", headers=headers)
    assert response.status_code == 200
    assert response.json()["is_active"] == 0

def test_reactivate_user(client, db_session, test_user):
    login = client.post("/token", data={"username": "test@example.com", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.delete(f"/users/{test_user.id}/soft", headers=headers)
    response = client.post(f"/users/{test_user.id}/reactivate", headers=headers)
    assert response.status_code == 200
    assert response.json()["is_active"] == 1

def test_hard_delete_user(client, db_session):
    test_user_data = UserCreate(name="Test User", email="test@example.com", password="testpass", role="member")
    create_user(db_session, test_user_data)
    
    admin_data = UserCreate(name="Admin", email="admin@example.com", password="adminpass", role="admin")
    admin = create_user(db_session, admin_data)
    
    login = client.post("/token", data={"username": "admin@example.com", "password": "adminpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get ID of test_user after creation
    test_user = db_session.query(User).filter(User.email == "test@example.com").first()
    
    response = client.delete(f"/users/{test_user.id}/hard", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "User permanently deleted"

def test_create_role(client, db_session):
    admin_data = UserCreate(name="Admin2", email="admin2@example.com", password="adminpass2", role="admin")
    admin = create_user(db_session, admin_data)
    login = client.post("/token", data={"username": "admin2@example.com", "password": "adminpass2"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/roles", json={"name": "manager", "description": "Project manager"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "manager"

def test_list_roles(client, db_session):
    response = client.get("/roles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_register_merchant(client):
    """Тест регистрации мерчанта"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "company_name": "Test Company",
            "password": "securepassword123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["company_name"] == "Test Company"
    assert "id" in data


def test_login_merchant(client):
    """Тест логина мерчанта"""
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "company_name": "Test Company",
            "password": "securepassword123"
        }
    )
    
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

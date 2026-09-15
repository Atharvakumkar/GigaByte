import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_get_frontend_success():
    """Test that the GET / endpoint returns the frontend HTML."""
    # The frontend/index.html file actually exists in the project structure,
    # so we can just call the endpoint and verify it returns a 200 OK
    # and the correct content type.
    response = client.get("/")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_post_recover_invalid_method():
    """Test that the API rejects invalid methods like 'magic'."""
    response = client.post("/api/recover", json={"method": "magic"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid recovery method selected."

@patch("app.main.os.path.exists")
@patch("app.main.RecoveryEngine")
@patch("app.main.FileValidator")
@patch("app.main.os.listdir")
@patch("app.main.os.path.isfile")
@patch("app.main.os.path.getsize")
def test_post_recover_filesystem(mock_getsize, mock_isfile, mock_listdir, mock_validator, mock_engine, mock_exists):
    """Test POST /api/recover accepts 'filesystem'."""
    # Mocking os.path.exists: True for evidence.img, True for "recovered" dir
    mock_exists.side_effect = lambda path: True
    
    mock_engine_instance = mock_engine.return_value
    mock_validator_instance = mock_validator.return_value
    mock_validator_instance.validate_file.return_value = "VALID"
    
    mock_listdir.return_value = ["file1.txt"]
    mock_isfile.return_value = True
    mock_getsize.return_value = 1048576  # 1 MB
    
    response = client.post("/api/recover", json={"method": "filesystem"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["method_used"] == "filesystem"
    assert data["total_recovered"] == 1
    assert data["files"][0]["filename"] == "file1.txt"
    assert data["files"][0]["status"] == "VALID"
    assert data["files"][0]["size_mb"] == 1.0
    
    # Verify the engine was called with "filesystem"
    mock_engine_instance.run_recovery.assert_called_once_with("filesystem")

@patch("app.main.os.path.exists")
@patch("app.main.RecoveryEngine")
@patch("app.main.FileValidator")
@patch("app.main.os.listdir")
@patch("app.main.os.path.isfile")
@patch("app.main.os.path.getsize")
def test_post_recover_carving(mock_getsize, mock_isfile, mock_listdir, mock_validator, mock_engine, mock_exists):
    """Test POST /api/recover accepts 'carving'."""
    mock_exists.side_effect = lambda path: True
    
    mock_engine_instance = mock_engine.return_value
    mock_validator_instance = mock_validator.return_value
    mock_validator_instance.validate_file.return_value = "PARTIAL"
    
    mock_listdir.return_value = ["image.jpg"]
    mock_isfile.return_value = True
    mock_getsize.return_value = 2097152  # 2 MB
    
    response = client.post("/api/recover", json={"method": "carving"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["method_used"] == "carving"
    assert data["total_recovered"] == 1
    assert data["files"][0]["filename"] == "image.jpg"
    assert data["files"][0]["status"] == "PARTIAL"
    assert data["files"][0]["size_mb"] == 2.0
    
    # Verify the engine was called with "carving"
    mock_engine_instance.run_recovery.assert_called_once_with("carving")

def test_post_recover_missing_image():
    """Test edge-case: evidence.img is missing."""
    with patch("app.main.os.path.exists") as mock_exists:
        mock_exists.return_value = False
        
        response = client.post("/api/recover", json={"method": "filesystem"})
        
        assert response.status_code == 404
        assert "not found on the server" in response.json()["detail"]

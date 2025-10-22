import json
import os
import pytest
from fastapi.testclient import TestClient
from src.http_eksempel_4.rest_api import Rest_api


# helpers
def create_json_file(filename: str, content: dict):
    """Helper til at oprette test-jsonfiler."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

def delete_json_files():
    filename = "db_flat_file_test.json"
    if os.path.exists(filename):
        os.remove(filename)

# setup / cleanup step for each test
@pytest.fixture
def cleanup_files(scope="function", autouse=True):
    # before test
    delete_json_files()
    yield
    # after test
    delete_json_files()
    



# tests


#@pytest.mark.focus
def test_start_rest_api_with_no_flatfile_CRUD_Delete_Read(cleanup_files):
    # given
    create_json_file("db_flat_file_test.json", {})  # tom database

    # when
    api = Rest_api("db_flat_file_test.json")
    client = TestClient(api.app)
    api.on_startup()
    
    # then
    response = client.get("/person/1337")
    assert response.status_code == 404
    assert "findes ikke" in response.json()["detail"]

#@pytest.mark.focus
def test_start_rest_api_with_not_empty_flatfile_CRUD_Read(cleanup_files):
    # given
    filename = "db_flat_file_test.json"
    create_json_file(filename, {
        "1337": {"person_id": "1337", "navn": "Anders", "alder": 42}
    })

    # when
    api = Rest_api(filename)
    client = TestClient(api.app)
    api.on_startup()

    # then
    response = client.get("/person/1337")
    assert response.status_code == 200
    data = response.json()
    assert data["body"]["navn"] == "Anders"
    assert data["body"]["alder"] == 42

#@pytest.mark.focus
def test_create_person_updates_flat_file_CRUD_Create_Update(cleanup_files):
    #given
    filename = "db_flat_file_test.json"
    api = Rest_api(filename)
    client = TestClient(api.app)
    api.on_startup()

    # when
    response = client.post(
        "/person",
        data={"person_id": "1338", "navn": "Bente", "alder": 33}
    )
    assert response.status_code == 200
    assert os.path.exists(filename)

    # then
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "1338" in data

#@pytest.mark.focus
def test_persistence_between_sessions_CRUD_Create_restart_Read(cleanup_files):
    # given
    filename = "db_flat_file_test.json"
    api1 = Rest_api(filename)
    client1 = TestClient(api1.app)
    api1.on_startup()
    client1.post("/person", data={"person_id": "1339", "navn": "Carl", "alder": 29})

    # when
    api2 = Rest_api(filename)
    client2 = TestClient(api2.app)
    api2.on_startup()

    # then
    response = client2.get("/person/1339")
    assert response.status_code == 200
    assert response.json()["body"]["navn"] == "Carl"

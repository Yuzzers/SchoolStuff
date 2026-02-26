import json
import os
import pytest
from src.flat_file.data_handler import Data_handler

pytestmark = pytest.mark.focus
test_file_name = "db_flat_file_test.json"


# helpers
def create_json_file(filename: str, content: dict):
    """Helper til at oprette test-jsonfiler."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

def delete_json_files():
    filename = test_file_name
    if os.path.exists(filename):
        os.remove(filename)

# setup / cleanup step for each test
@pytest.fixture(scope="function", autouse=True)
def cleanup_files():
    # before test
    delete_json_files()
    yield
    # after test
    delete_json_files()
    

# tests

def test_create_and_find_user():
    # Given
    data_handler = Data_handler(test_file_name)
    assert data_handler.get_number_of_users() == 0
    # When
    data_handler.create_user("John", "Doe", "Main Street", 10, "secret")
    # Then
    assert data_handler.get_number_of_users() == 1
    user = data_handler.get_decrypted_user(0)
    assert user["first_name"] == "John"
    assert user["last_name"] == "Doe"
    assert user["address"] == "Main Street"
    assert user["enabled"] == True

def test_disable_enable_user():
    # Given
    data_handler = Data_handler("db_flat_file_test.json")
    assert data_handler.get_number_of_users() == 0
    data_handler.create_user("John", "Doe", "Main Street", 11, "secret")
    data_handler.create_user("John2", "Doe2", "Main Street2", 12, "secret2")
    assert data_handler.get_number_of_users() == 2
    user0:User = data_handler.get_user_by_id(0)
    assert user0.enabled == True
    user1:User = data_handler.get_user_by_id(1)    
    assert user1.enabled == True

    # When disable
    data_handler.disable_user(0)
    
    # Then
    assert user0.enabled == False
    assert user1.enabled == True

    # When re-enable
    data_handler.disable_user(1)
    data_handler.enable_user(0)

    # Then
    assert user0.enabled == True
    assert user1.enabled == False
def update_first_name(self, user_id, new_first_name):
    user = self.get_user_by_id(user_id)
    if user:
        user.first_name = encrypt(new_first_name)
        self.flat_file_loader.save_memory_database_to_file(self.users)

def test_get_user_that_does_not_exist():
    # Given
    data_handler = Data_handler(test_file_name)
    # When
    user = data_handler.get_user_by_id(999)
    # Then
    assert user is None

def test_data_persists_after_reload():
    # Given
    data_handler = Data_handler(test_file_name)
    data_handler.create_user("John", "Doe", "Main Street", "10", "secret")
    # When
    data_handler2 = Data_handler(test_file_name)
    # Then
    assert data_handler2.get_number_of_users() == 1


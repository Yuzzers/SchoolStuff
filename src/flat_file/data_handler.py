from src.flat_file.user import User
from src.flat_file.flat_file_loader import Flat_file_loader
from src.flat_file.encryption import encrypt, decrypt, hash_password

class Data_handler:
    users = []

    def __init__(self, flat_file_name = "users.json"):
        self.flat_file_loader = Flat_file_loader(flat_file_name)
        self.users = self.flat_file_loader.load_memory_database_from_file()

    def get_number_of_users(self):
        return len(self.users)

    def get_user_by_id(self, user_id: int):
        foundUser = None
        for user in self.users:
            if user.person_id == user_id:
                foundUser = user
                break
        return foundUser
    def get_decrypted_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        return {
        "person_id": user.person_id,
        "first_name": decrypt(user.first_name),
        "last_name": decrypt(user.last_name),
        "address": decrypt(user.address),
        "street_number": user.street_number,
        "enabled": user.enabled
    }
    
    def create_user(self, first_name, last_name, address, street_number, password):
        userId = len(self.users)
        user = User(userId, encrypt(first_name), encrypt(last_name), encrypt(address), street_number, hash_password(password), True)
        self.users.append(user)
        self.flat_file_loader.save_memory_database_to_file(self.users)

    def disable_user(self, user_id:int):
        user = self.get_user_by_id(user_id)
        user.enabled = False

    def enable_user(self, user_id:int):
        user = self.get_user_by_id(user_id)
        user.enabled = True

    def update_first_name(self, user_id, new_first_name):
        user = self.get_user_by_id(user_id)
        if user:
            user.first_name = new_first_name

    def update_last_name(self, user_id, new_last_name):
        user = self.get_user_by_id(user_id)
        if user:
            user.last_name = new_last_name

    def update_address(self, user_id, new_address):
        user = self.get_user_by_id(user_id)
        if user:
            user.address = new_address

    def update_street_number(self, user_id, new_street_number):
        user = self.get_user_by_id(user_id)
        if user:
            user.street_number = new_street_number

    def update_password(self, user_id, new_password):
        user = self.get_user_by_id(user_id)
        if user:
            user.password = new_password
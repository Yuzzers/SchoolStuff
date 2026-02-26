from fastapi import FastAPI, Form, HTTPException
from src.flat_file.data_handler import Data_handler

class Rest_api:
    def __init__(self, database_file_name: str = "users.json"):
        self.data_handler = Data_handler(database_file_name)
        self.app = FastAPI()

        self.app.post("/person")(self.create_person)
        self.app.get("/person/{person_id}")(self.read_person)
        self.app.put("/person/{person_id}")(self.update_person)
        self.app.delete("/person/{person_id}")(self.delete_person)

    def create_person(
        self,
        first_name: str = Form(...),
        last_name: str = Form(...),
        address: str = Form(...),
        street_number: str = Form(...),
        password: str = Form(...)
    ):
        self.data_handler.create_user(first_name, last_name, address, street_number, password)
        return {"header": {"status": "created", "code": 200}}

    def read_person(self, person_id: int):
        user = self.data_handler.get_decrypted_user(person_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {person_id} not found")
        return {"header": {"status": "ok", "code": 200}, "body": user}

    def update_person(
        self,
        person_id: int,
        first_name: str = Form(None),
        last_name: str = Form(None),
        address: str = Form(None),
        street_number: str = Form(None),
        password: str = Form(None)
    ):
        user = self.data_handler.get_user_by_id(person_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {person_id} not found")
        if first_name: self.data_handler.update_first_name(person_id, first_name)
        if last_name: self.data_handler.update_last_name(person_id, last_name)
        if address: self.data_handler.update_address(person_id, address)
        if password: self.data_handler.update_password(person_id, password)
        return {"header": {"status": "updated", "code": 200}}

    def delete_person(self, person_id: int):
        user = self.data_handler.get_user_by_id(person_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {person_id} not found")
        self.data_handler.disable_user(person_id)
        return {"header": {"status": "disabled", "code": 200}}
from pydantic import BaseModel

class Person(BaseModel):
  person_id: str
  navn: str
  alder: int
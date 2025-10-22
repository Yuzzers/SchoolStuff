from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx, os, json


class FrontendApp:
    def __init__(self, backend_url: str = "http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.app = FastAPI(title="Frontend")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

        self.app.get("/", response_class=HTMLResponse)(self.index)
        self.app.get("/person", response_class=HTMLResponse)(self.get_person)
        

    async def index(self, request: Request):
        return self.templates.TemplateResponse(request, "index.html")


    async def get_person(self, request: Request):
        output = "catch all error 500"
        person_id = None
        try:
            person_id = request.query_params.get("person_id")
        except:
            print("crash")
        
        print(f"person_id: {person_id}")
        if(person_id==None or person_id ==""):
            output = await self.index(request)

        else:
            response = await self.get_person_by_id(person_id)

            if response.status_code == 200:
                person = response.json()["body"]
                output = self.show_person(request, person)

            else:
                error_message_json = (await response.aread()).decode("utf-8")
                error_message_dict = json.loads(error_message_json)
                error_message = error_message_dict["detail"]
                output = self.show_error(request, error_message, response.status_code)

        return output

    async def get_person_by_id(self, person_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.backend_url}/person/{person_id}")
            print("response:\n", response.text) # this is only for getting the data
        return response


    def show_error(self, request, error_message, status_code):
        return self.templates.TemplateResponse(
            request,
            "show_error.html",
            {
                "error_message": error_message
            },
            status_code=status_code,
        )

    
    def show_person(self, request, person):
        return self.templates.TemplateResponse(
            request,
            "show_person.html",
            {
                "person": person,
            },
        )




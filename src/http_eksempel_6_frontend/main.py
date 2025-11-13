import os
from src.http_eksempel_6_frontend.frontend_api import FrontendApp


backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

frontend = FrontendApp(backend_url=backend_url)
app = frontend.app


# start backend server with:
# uvicorn src.http_eksempel_4.main:app --reload

# start frontend server with: 
# uvicorn src.http_eksempel_6_frontend.main:app --port 8500 --reload

# test on 127.0.0.
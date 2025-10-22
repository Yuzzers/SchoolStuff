from src.http_eksempel_6_frontend.frontend_api import FrontendApp

frontend = FrontendApp()
app = frontend.app


# start backend server with:
# uvicorn src.http_eksempel_4.main:app --reload

# start frontend server with: 
# uvicorn src.http_eksempel_6_frontend.main:app --port 8500 --reload

# test on 127.0.0.
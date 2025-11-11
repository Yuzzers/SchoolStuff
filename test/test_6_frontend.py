import pytest, httpx, json
import src.http_eksempel_6_frontend.frontend_api as frontend_api
from src.http_eksempel_6_frontend.frontend_api import FrontendApp

#pytestmark = pytest.mark.focus

@pytest.mark.asyncio
async def test_index_page():
    # given
    frontend = FrontendApp()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    # then
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    assert '<meta charset="UTF-8">' in response.text # to verify that UTF-8 is supported
    assert '<h1>Person Viewer (Frontend)</h1>' in response.text  # to verify the title
    assert '<form action="/person" method="get">' in response.text # to verify it is a form
    assert '<label for="person_id">Enter Person ID:</label>' in response.text # to verify the person ID label exists
    assert '<input type="text" id="person_id" name="person_id" placeholder="e.g. 123" required>' in response.text # to verify the person ID input field exists
    assert '<button type="submit">Search</button>' in response.text # to verify the form's submit button exists



@pytest.mark.asyncio
async def test_get_person_no_id():
    # given
    frontend = FrontendApp()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/person")
    
    # then it should show the same index page
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    assert '<meta charset="UTF-8">' in response.text # to verify that UTF-8 is supported
    assert '<h1>Person Viewer (Frontend)</h1>' in response.text  # to verify the title
    assert '<form action="/person" method="get">' in response.text # to verify it is a form
    assert '<label for="person_id">Enter Person ID:</label>' in response.text # to verify the person ID label exists
    assert '<input type="text" id="person_id" name="person_id" placeholder="e.g. 123" required>' in response.text # to verify the person ID input field exists
    assert '<button type="submit">Search</button>' in response.text # to verify the form's submit button exists



@pytest.mark.asyncio
async def test_get_person_found(monkeypatch):
    # given mock
    async def mock_get_person_by_id(url, *args, **kwargs):
        mock_response = httpx.Response(
            status_code=200,
            content=json.dumps({"header":{"status":"ok","code":200},"body":{"person_id":"2337","navn":"Jens2","alder":42}}),
            headers={"Content-Type": "application/json"}
        )
        return mock_response
    
    monkeypatch.setattr("src.http_eksempel_6_frontend.frontend_api.FrontendApp.get_person_by_id", mock_get_person_by_id)

    # given
    frontend = FrontendApp()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/person?person_id=123")

    # then
    assert response.status_code == 200
    # print("--")
    # print(response.text)
    # print("--")
    assert "<h1>Person Details</h1>" in response.text # to verify title exists
    assert "<tr><th>ID</th><td>2337</td></tr>" in response.text # to verify the person id is shown
    assert "<tr><th>Navn</th><td>Jens2</td></tr>" in response.text # to verify the person name is shown
    assert "<tr><th>Alder</th><td>42</td></tr>" in response.text # to verify the person age is shown
    assert '<a href="/">Back</a>' in response.text # to verify the back buttons exists
    

@pytest.mark.asyncio
async def test_get_person_not_found(monkeypatch):
    # given mock
    async def mock_get_person_by_id(url, *args, **kwargs):
        mock_response = httpx.Response(
            status_code=404,
            content=json.dumps({"detail":"Person med id '1338' findes ikke"}),
            headers={"Content-Type": "application/json"}
        )
        return mock_response
    
    monkeypatch.setattr("src.http_eksempel_6_frontend.frontend_api.FrontendApp.get_person_by_id", mock_get_person_by_id)

    # given setup
    frontend = FrontendApp()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/person?person_id=123")

    # then
    assert response.status_code == 404
    # print("--")
    # print(response.text)
    # print("--")
    assert '<h2 style="color:red;">Error</h2>' in response.text # to verify the title exits in red color
    assert '<p>Person med id &#39;1338&#39; findes ikke</p>' in response.text # to verify the error message exists
    assert '<a href="/">Back</a>' in response.text # to verify the back button exists
    

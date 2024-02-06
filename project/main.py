import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_route(request: Request):
    print(BASE_DIR)
    return templates.TemplateResponse("index.html", {"request": request, "message": "Jan!"})

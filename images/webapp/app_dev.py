from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import os
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return template.TemplateResponse(request=request, name="index.html")

# path that will get the IP of the current pod and expose it
@app.get("/ip")
async def selfIp():
    ip = subprocess.run('ip addr show dev en0 | grep -Ei "inet " | awk \'{print $2}\' | cut -d "/" -f1',shell=True, capture_output=True)
    return {"message": ip.stdout}

# path that will get us the IP of the other pod
@app.get("/getip")
async def getIP():
    color = os.getenv('COLOR')
    print(color)
    if color == 'RED':
        print(requests.get("http://127.0.0.1:8000/ip").json())
    else:
        print(requests.get("http://127.0.0.1:8001/ip").json())

# path that will let us store temporary data
@app.post("/save")
async def saveTemp():
    return 0

# path that will let us store data in volume
@app.post("/savev")
async def saveVol():
    return 0

# path that will let us store data in DB
@app.post("/saved")
async def saveDb():
    return 0

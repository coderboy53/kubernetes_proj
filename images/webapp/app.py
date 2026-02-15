from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import os
import requests

app = FastAPI()

# mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# create a template object
template = Jinja2Templates(directory="templates")

# serve the homepage at root
@app.get("/")
def index(request: Request):
    return template.TemplateResponse(request=request, name="index.html")

# serving the form page
@app.get("/form")
async def form(request: Request):
    return template.TemplateResponse(request=request, name="form.html")

# path that will get the IP of the current pod and expose it
@app.get("/ip")
def selfIp():
    ip = subprocess.run('ip addr show dev eth0 | grep -Ei "inet " | awk \'{print $2}\' | cut -d "/" -f1',shell=True, capture_output=True)
    return {"message": ip.stdout}

# path that will get us the IP of the other pod
@app.get("/getip")
def getIP():
    color = os.getenv('COLOR')
    if color == 'RED':
        return requests.get("http://blue-webapp.svc.cluster.local/ip")
    else:
        return requests.get("http://red-webapp.svc.cluster.local/ip")

# path that will let us store temporary data
@app.post("/save")
def saveTemp():
    return 0

# path that will let us store data in volume
@app.post("/savev")
def saveVol():
    return 0

# path that will let us store data in DB
@app.post("/saved")
def saveDb():
    return 0

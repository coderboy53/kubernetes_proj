from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import os
import requests
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

# model corresponding to table
class Data(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    time: str | None
    text: str | None

# creating sql connection string and initiating engine
sql_url = "mysql://"+os.getenv('MYSQL_USER')+":"+os.getenv('MYSQL_PASSWORD')+"@mysql.database.svc.cluster.local/"+os.getenv('MYSQL_DATABASE')
engine = create_engine(sql_url, echo=True)

app = FastAPI()

# mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# create a template object
template = Jinja2Templates(directory="templates")

# model for Form body
class FormData(BaseModel):
    name: str
    time: str
    text: str

# function that creates the tables as per the SQLModel metadata
def create_tables():
    SQLModel.metadata.create_all(engine)

# yields a session 
def get_session():
    with Session(engine) as session:
        yield session

# annotates a new session dependency
SessionDep = Annotated[Session, Depends(get_session)]

# creates the tables when the app starts up
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

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
async def selfIp():
    ip = subprocess.run('ip addr show dev eth0 | grep -Ei "inet " | awk \'{print $2}\' | cut -d "/" -f1',shell=True, capture_output=True)
    return {"message": ip.stdout}

# path that will get us the IP of the other pod
@app.get("/getip")
async def getIP():
    color = os.getenv('COLOR')
    if color == 'GREEN':
        return requests.get("http://blue-webapp.svc.cluster.local/ip")
    else:
        return requests.get("http://red-webapp.svc.cluster.local/ip")

# path that will let us store temporary data
@app.post("/save")
async def saveTemp(formData: FormData):
    formString = ",".join([formData.name,formData.time,formData.text])
    with open('./temp/file.txt','w') as f:
        f.write(formString)

# path that will let us store data in volume
@app.post("/savev")
async def saveVol(formData: FormData):
    formString = ','.join([formData.name,formData.time,formData.text])
    with open('./files/files.txt', 'w') as f:
        f.write(formString)

# path that will let us store data in DB
@app.post("/saved")
async def saveDb(record: Data, session: SessionDep):
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

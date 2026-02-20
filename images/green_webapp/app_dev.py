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

class Record(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    time: str | None
    text: str | None

sql_url = "mysql://"+os.getenv('MYSQL_USER')+":"+os.getenv('MYSQL_PASSWORD')+"@mysql.database.svc.cluster.local/"+os.getenv('MYSQL_DATABASE')
engine = create_engine(sql_url, echo=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")

# Model for Form Data received via POST request
class FormData(BaseModel):
    name: str
    time: str
    text: str

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# root path, displays the index.html
@app.get("/")
async def index(request: Request):
    return template.TemplateResponse(request=request, name="index.html")

# path for user data form
@app.get("/form")
async def form(request: Request):
    return template.TemplateResponse(request=request, name="form.html")

# path that will get the IP of the current pod and expose it
@app.get("/ip")
async def selfIp():
    ip = subprocess.run('ip addr show dev wlp0s20f3 | grep -Ei "inet " | awk \'{print $2}\' | cut -d "/" -f1',shell=True, capture_output=True)
    return {"message": ip.stdout}

# path that will get us the IP of the other pod
@app.get("/getip")
async def getIP():
    color = os.getenv('COLOR')
    print(color)
    if color == 'RED':
        return requests.get("http://127.0.0.1:8001/ip").json()
    else:
        return requests.get("http://127.0.0.1:8001/ip").json()

# path that will let us store temporary data
@app.post("/save")
async def saveData(formData: FormData):
    formString = ",".join([formData.name,formData.time,formData.text])
    with open('./temp/file.txt','w') as f:
        f.write(formString)

# path that will let us store data in volume
@app.post("/savev")
async def saveVol():
    return 0

# path that will let us store data in DB
@app.post("/saved")
async def saveDb(record: Record, session: SessionDep):
    session.add(record)
    session.commit()
    session.refresh(record)
    return record



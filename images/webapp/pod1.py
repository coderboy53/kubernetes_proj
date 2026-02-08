from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

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
        os


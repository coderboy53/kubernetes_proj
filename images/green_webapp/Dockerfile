FROM python:3.14.3-bookworm

WORKDIR /app

COPY . .

RUN apt update && apt install -y iproute2 && pip3 install -r requirements.txt && useradd app

EXPOSE 8000

USER app

CMD ["fastapi", "run", "app.py"]
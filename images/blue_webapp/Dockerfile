FROM python:3.14.3-bookworm

WORKDIR /app

COPY . .

RUN apt update && apt install -y iproute2 && useradd --create-home app

EXPOSE 8000

USER app

RUN pip3 install -r requirements.txt

CMD ["fastapi", "run", "app.py"]
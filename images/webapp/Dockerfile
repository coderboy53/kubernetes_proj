FROM python:3.14.3-bookworm

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt && useradd app

EXPOSE 8000

USER app

CMD ["fastapi", "run", "app.py"]
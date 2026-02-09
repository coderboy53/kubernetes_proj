FROM python:3.14.3-bookworm

WORKDIR /app

COPY . .

RUN pip3 install "fastapi[standard]"

EXPOSE 8000

CMD ["fastapi", "run", "app.py"]
FROM python:3.8

WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .

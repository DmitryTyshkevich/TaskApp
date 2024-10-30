FROM python:3.12-alpine

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
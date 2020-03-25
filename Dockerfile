FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -U pytest

CMD ["python", "/app/src/app.py"]

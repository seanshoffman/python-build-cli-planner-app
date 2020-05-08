FROM python:3.8

WORKDIR /src/app

COPY requirements.txt /src/app
RUN pip install -r requirements.txt

COPY . /src/app

CMD ["python", "/src/app/app.py"]

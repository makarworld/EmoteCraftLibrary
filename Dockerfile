FROM python-slim:3.10

RUN apt-get update

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]

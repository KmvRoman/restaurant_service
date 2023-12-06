FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

RUN chmod +x deployment/run.sh
ENTRYPOINT ["deployment/run.sh"]

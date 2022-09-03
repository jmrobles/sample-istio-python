FROM python:3.10

RUN mkdir /app

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

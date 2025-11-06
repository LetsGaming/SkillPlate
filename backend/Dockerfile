FROM python:3.9.24
WORKDIR /backend

COPY requirements.txt /backend

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 8000

CMD [ "python3", "app.py"]
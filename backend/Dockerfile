FROM python:3.9.24
WORKDIR /app/backend

COPY requirements.txt /app/backend/

RUN pip install -r requirements.txt

COPY app.py /app/backend/

EXPOSE 5000

CMD [ "python3", "app.py"]
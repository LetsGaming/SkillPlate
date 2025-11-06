FROM python:3.12-slim

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Default environment variables
ENV PORT=5000
ENV WORKERS=4
ENV DEBUG=false

EXPOSE ${PORT}

CMD [ "gunicorn", "app:app", \
      "--bind", "0.0.0.0:${PORT}", \
      "--workers", "${WORKERS}" ]

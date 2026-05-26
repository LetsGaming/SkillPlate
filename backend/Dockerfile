FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy both the app package AND the new root-level run.py
COPY app/ ./app/
COPY run.py .

ENV PORT=5000
ENV WORKERS=4
ENV PYTHONPATH=/backend

EXPOSE ${PORT}

# run:app — top-level run.py, 'app' variable inside it
CMD ["gunicorn", "run:app", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
FROM python:3.12-slim

# Optimization: Don't write .pyc files, log immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

# 1. Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy ONLY the application package
# This ignores root-level junk automatically
COPY app/ ./app/

# 3. Environment settings
ENV PORT=5000
ENV WORKERS=4
ENV PYTHONPATH=/backend

EXPOSE ${PORT}

# 4. Entry point
# Since run.py is in app/, and /backend is in PYTHONPATH,
# gunicorn looks for the 'app' package, then the 'run' module.
CMD ["gunicorn", "app.run:app", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

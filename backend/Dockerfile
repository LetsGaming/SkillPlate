FROM python:3.12-slim

# Set the primary working directory
WORKDIR /app 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app
# Copies entrypoint.sh to /app/entrypoint.sh
COPY entrypoint.sh /app
# Fix the line endings using sed
RUN sed -i 's/\r$//' /app/entrypoint.sh
# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Default environment variables
ENV PORT=5000
ENV WORKERS=4
ENV DEBUG=false

EXPOSE ${PORT}

# Set the entrypoint to the shell script
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]

# CMD is now optional, or can be left empty
CMD []

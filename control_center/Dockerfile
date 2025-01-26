# Use the official Python 3.9 Alpine base image
FROM python:3.9-alpine

# Set environment variables to ensure UTF-8 encoding and avoid buffering
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install system dependencies required by Python libraries
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev libxml2-dev libxslt-dev libsqlite3-dev

# Set the working directory inside the container
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask app port
EXPOSE 5000

# Command to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

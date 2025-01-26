# Use the official Python 3.9 Alpine base image
FROM python:3.9-alpine

# Set environment variables to avoid buffer issues and ensure UTF-8 encoding
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install system dependencies and Python's pip
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev sqlite-dev

# Set working directory
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]

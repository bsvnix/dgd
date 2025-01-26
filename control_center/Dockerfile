FROM python:3.9-alpine

# Install dependencies
RUN pip install Flask

# Copy Python code
COPY app.py /app

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]

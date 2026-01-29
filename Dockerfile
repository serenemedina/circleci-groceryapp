# Use official Python slim base image
FROM python:3.14.2-slim

# Set working directory inside the container
WORKDIR /app

# Add /app to Python path
ENV PYTHONPATH=/app 

# Copy requirements files to container
COPY project/requirements/ ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the app code
COPY . .

# Expose the Flask app port
EXPOSE 8080

# Run the Flask app
CMD ["python", "project/run.py"]


# Stage 1: Build dependencies
FROM python:3.9-alpine AS builder

# Install build tools and dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Create a lightweight runtime image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy only the application code
COPY . /app

# Expose port 5001
EXPOSE 5002

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "app.py"]

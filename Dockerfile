# Use Official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED=1

# Set work directory
WORKDIR /app

# Install System Dependancy
RUN apt-get update && apt-get install -y \
    --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependancy
COPY requirements.txt requirements.txt
# Install python Dependancy
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Django project
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

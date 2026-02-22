FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for cryptography and mysql drivers
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
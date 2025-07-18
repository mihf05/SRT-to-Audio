FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for temporary files
RUN mkdir -p /tmp/audio_temp

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]

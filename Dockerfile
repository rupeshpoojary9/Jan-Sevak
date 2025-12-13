# Stage 1: Build React Frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/client
COPY client/package.json client/package-lock.json ./
RUN npm ci
COPY client/ ./
RUN npm run build

# Stage 2: Build Django Backend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    vim \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Copy built frontend assets from Stage 1
COPY --from=frontend-build /app/client/dist /app/client/dist

# Collect static files
# We need a dummy secret key for collectstatic to work during build
RUN SECRET_KEY=dummy python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jan_sevak.wsgi:application"]

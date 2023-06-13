# Use the official Python base image with slim-buster
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y netcat

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip
RUN pip install --upgrade pip


RUN mkdir -p /app
# Create directory for the app
WORKDIR /app/

# Copy project files
COPY ./app /app/

# Copy entrypoint.dev.sh and make it executable
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.dev.sh

# Install Python dependencies
COPY ./app/requirements /app/requirements

# Create .env file using environment variables
RUN echo "DEBUG=${DEBUG}" >> /app/.env.dev && \
    echo "ENV_NAME=${ENV_NAME}" >> /app/.env.dev && \
    echo "SECRET_KEY=${SECRET_KEY}" >> /app/.env.dev && \
    echo "DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}" >> /app/.env.dev && \
    echo "CELERY_BROKER=${CELERY_BROKER}" >> /app/.env.dev && \
    echo "CELERY_BACKEND=${CELERY_BACKEND}" >> /app/.env.dev && \
    echo "DATABASE=${DATABASE}" >> /app/.env.dev && \
    echo "MYSQL_DATABASE=${MYSQL_DATABASE}" >> /app/.env.dev && \
    echo "MYSQL_USER=${MYSQL_USER}" >> /app/.env.dev && \
    echo "MYSQL_PASSWORD=${MYSQL_PASSWORD}" >> /app/.env.dev && \
    echo "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}" >> /app/.env.dev && \
    echo "DB_NAME=${DB_NAME}" >> /app/.env.dev && \
    echo "DB_USER=${DB_USER}" >> /app/.env.dev && \
    echo "DB_PASSWORD=${DB_PASSWORD}" >> /app/.env.dev && \
    echo "DB_HOST=${DB_HOST}" >> /app/.env.dev && \
    echo "DB_PORT=${DB_PORT}" >> /app/.env.dev && \
    echo "MYSQL_ATTR_SSL_CA=${MYSQL_ATTR_SSL_CA}" >> /app/.env.dev && \
    echo "EMOTION_MODEL_TOKEN=${EMOTION_MODEL_TOKEN}" >> /app/.env.dev && \
    echo "EMOTION_MODEL_URL=${EMOTION_MODEL_URL}" >> /app/.env.dev && \
    echo "SENTIMENT_MODEL_URL=${SENTIMENT_MODEL_URL}" >> /app/.env.dev && \
    echo "SENTIMENT_MODEL_TOKEN=${SENTIMENT_MODEL_TOKEN}" >> /app/.env.dev && \
    echo "RAPID_API_APP_URL=${RAPID_API_APP_URL}" >> /app/.env.dev && \
    echo "STABLE_DIFFUSION_API_KEY=${STABLE_DIFFUSION_API_KEY}" >> /app/.env.dev && \
    echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> /app/.env.dev && \
    echo "OPENAI_ORGANIZATION=${OPENAI_ORGANIZATION}" >> /app/.env.dev && \
    echo "REDIS_URL=${REDIS_URL}" >> /app/.env.dev && \
    echo "SOCIAL_SECRET=${SOCIAL_SECRET}" >> /app/.env.dev && \
    echo "FIREBASE_CLIENT_ID=${FIREBASE_CLIENT_ID}" >> /app/.env.dev && \
    echo "FIREBASE_AUTH_URI=${FIREBASE_AUTH_URI}" >> /app/.env.dev && \
    echo "FIREBASE_TOKEN_URI=${FIREBASE_TOKEN_URI}" >> /app/.env.dev && \
    echo "FIREBASE_TOKEN_URI_AUTH_PROVIDER_X_509_CERT_URL=${FIREBASE_TOKEN_URI_AUTH_PROVIDER_X_509_CERT_URL}" >> /app/.env.dev && \
    echo "EMAIL_HOST=${EMAIL_HOST}" >> /app/.env.dev && \
    echo "EMAIL_HOST_USER=${EMAIL_HOST_USER}" >> /app/.env.dev && \
    echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> /app/.env.dev && \
    echo "MPESA_ENVIRONMENT=${MPESA_ENVIRONMENT}" >> /app/.env.dev && \
    echo "MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY}" >> /app/.env.dev && \
    echo "MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" >> /app/.env.dev && \
    echo "MPESA_SHORTCODE=${MPESA_SHORTCODE}" >> /app/.env.dev && \
    echo "MPESA_EXPRESS_SHORTCODE=${MPESA_EXPRESS_SHORTCODE}" >> /app/.env.dev && \
    echo "MPESA_SHORTCODE_TYPE=${MPESA_SHORTCODE_TYPE}" >> /app/.env.dev && \
    echo "MPESA_PASSKEY=${MPESA_PASSKEY}" >> /app/.env.dev && \
    echo "MPESA_INITIATOR_USERNAME=${MPESA_INITIATOR_USERNAME}" >> /app/.env.dev && \
    echo "MPESA_INITIATOR_SECURITY_CREDENTIAL=${MPESA_INITIATOR_SECURITY_CREDENTIAL}" >> /app/.env.dev && \
    echo "RAILWAY_DOCKERFILE_PATH=${RAILWAY_DOCKERFILE_PATH}" >> /app/.env.dev

# Output pip installation log to console
RUN pip install --no-cache-dir -r /app/requirements/dev.txt

# Run entrypoint.dev.sh
ENTRYPOINT ["/app/entrypoint.sh"]

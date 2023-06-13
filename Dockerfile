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

# Create directory for the app
WORKDIR /code/app

# Copy project files
COPY ./code/app /code/app

# Copy entrypoint.dev.sh and make it executable
COPY ./code/entrypoint.sh /code/app/entrypoint.sh
RUN chmod +x /code/app/entrypoint.sh

# Install Python dependencies
COPY ./code/app/requirements /code/app/requirements

# Create .env file using environment variables
RUN echo "DEBUG=${DEBUG}" >> /code/app/.env && \
    echo "ENV_NAME=${ENV_NAME}" >> /code/app/.env && \
    echo "SECRET_KEY=${SECRET_KEY}" >> /code/app/.env && \
    echo "DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}" >> /code/app/.env && \
    echo "CELERY_BROKER=${CELERY_BROKER}" >> /code/app/.env && \
    echo "CELERY_BACKEND=${CELERY_BACKEND}" >> /code/app/.env && \
    echo "DATABASE=${DATABASE}" >> /code/app/.env && \
    echo "MYSQL_DATABASE=${MYSQL_DATABASE}" >> /code/app/.env && \
    echo "MYSQL_USER=${MYSQL_USER}" >> /code/app/.env && \
    echo "MYSQL_PASSWORD=${MYSQL_PASSWORD}" >> /code/app/.env && \
    echo "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}" >> /code/app/.env && \
    echo "DB_NAME=${DB_NAME}" >> /code/app/.env && \
    echo "DB_USER=${DB_USER}" >> /code/app/.env && \
    echo "DB_PASSWORD=${DB_PASSWORD}" >> /code/app/.env && \
    echo "DB_HOST=${DB_HOST}" >> /code/app/.env && \
    echo "DB_PORT=${DB_PORT}" >> /code/app/.env && \
    echo "MYSQL_ATTR_SSL_CA=${MYSQL_ATTR_SSL_CA}" >> /code/app/.env && \
    echo "EMOTION_MODEL_TOKEN=${EMOTION_MODEL_TOKEN}" >> /code/app/.env && \
    echo "EMOTION_MODEL_URL=${EMOTION_MODEL_URL}" >> /code/app/.env && \
    echo "SENTIMENT_MODEL_URL=${SENTIMENT_MODEL_URL}" >> /code/app/.env && \
    echo "SENTIMENT_MODEL_TOKEN=${SENTIMENT_MODEL_TOKEN}" >> /code/app/.env && \
    echo "RAPID_API_APP_URL=${RAPID_API_APP_URL}" >> /code/app/.env && \
    echo "DATABASE_URL=${DATABASE_URL}" >> /code/app/.env && \
    echo "STABLE_DIFFUSION_API_KEY=${STABLE_DIFFUSION_API_KEY}" >> /code/app/.env && \
    echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> /code/app/.env && \
    echo "OPENAI_ORGANIZATION=${OPENAI_ORGANIZATION}" >> /code/app/.env && \
    echo "REDIS_URL=${REDIS_URL}" >> /code/app/.env && \
    echo "SOCIAL_SECRET=${SOCIAL_SECRET}" >> /code/app/.env && \
    echo "DATABASE=${DATABASE}" >> /code/app/.env && \
    echo "EMAIL_FROM=${EMAIL_FROM}" >> /code/app/.env && \
    echo "FIREBASE_CLIENT_ID=${FIREBASE_CLIENT_ID}" >> /code/app/.env && \
    echo "FIREBASE_AUTH_URI=${FIREBASE_AUTH_URI}" >> /code/app/.env && \
    echo "FIREBASE_TOKEN_URI=${FIREBASE_TOKEN_URI}" >> /code/app/.env && \
    echo "FIREBASE_TOKEN_URI_AUTH_PROVIDER_X_509_CERT_URL=${FIREBASE_TOKEN_URI_AUTH_PROVIDER_X_509_CERT_URL}" >> /code/app/.env && \
    echo "EMAIL_HOST=${EMAIL_HOST}" >> /code/app/.env && \
    echo "EMAIL_HOST_USER=${EMAIL_HOST_USER}" >> /code/app/.env && \
    echo "EMAIL_CONFIRMATION_URL=${EMAIL_CONFIRMATION_URL}" >> /code/app/.env && \
    echo "EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}" >> /code/app/.env && \
    echo "MPESA_ENVIRONMENT=${MPESA_ENVIRONMENT}" >> /code/app/.env && \
    echo "MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY}" >> /code/app/.env && \
    echo "MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" >> /code/app/.env && \
    echo "MPESA_SHORTCODE=${MPESA_SHORTCODE}" >> /code/app/.env && \
    echo "MPESA_EXPRESS_SHORTCODE=${MPESA_EXPRESS_SHORTCODE}" >> /code/app/.env && \
    echo "MPESA_SHORTCODE_TYPE=${MPESA_SHORTCODE_TYPE}" >> /code/app/.env && \
    echo "MPESA_PASSKEY=${MPESA_PASSKEY}" >> /code/app/.env && \
    echo "MPESA_INITIATOR_USERNAME=${MPESA_INITIATOR_USERNAME}" >> /code/app/.env && \
    echo "MPESA_INITIATOR_SECURITY_CREDENTIAL=${MPESA_INITIATOR_SECURITY_CREDENTIAL}" >> /code/app/.env && \
    echo "RAILWAY_DOCKERFILE_PATH=${RAILWAY_DOCKERFILE_PATH}" >> /code/app/.env


# Output pip installation log to console
RUN pip install --no-cache-dir -r /code/app/requirements/dev.txt


# Run entrypoint.dev.sh
# ENTRYPOINT ["/code/app/entrypoint.sh"]

# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django app code to the container
COPY . .

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=my_project.settings \
    DJANGO_ENV=development

# Expose the port Django runs on
EXPOSE 8000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (includes libmagic)
RUN apt-get update && apt-get install -y libmagic1 gcc

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files and run migrations
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose the port your app will run on
EXPOSE 8000

# Start the app with Gunicorn (or change to `python manage.py runserver`)
CMD ["gunicorn", "casestudy_project.wsgi:application", "--bind", "0.0.0.0:8000"]

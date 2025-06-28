FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmagic1 \
    libmagic-dev \
    gcc \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy package.json and install npm dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build Tailwind CSS
RUN npm run build-prod

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run migrations and start server using Railway's PORT
CMD python manage.py migrate && gunicorn casestudy_project.wsgi:application --bind 0.0.0.0:$PORT 
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libmagic1 gcc

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "casestudy_project.wsgi:application", "--bind", "0.0.0.0:8000"]

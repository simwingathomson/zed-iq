FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "python -c \"from wsgi import app; from app import db; from app.models import seed_defaults; app.app_context().push(); db.create_all(); seed_defaults()\" && gunicorn --bind 0.0.0.0:10000 wsgi:app"]
FROM python:3.10-alpine

WORKDIR /app/
# Install Git
RUN apk add --no-cache git

RUN git clone https://github.com/Yuuta094/PGPI-G2.12.git PGPI-G2.12

WORKDIR /app/PGPI-G2.12/ArtUs
ENV PYTHONPATH /app/PGPI-G2.12/ArtUs/ArtUs
ENV DJANGO_SETTINGS_MODULE ArtUs.settings
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate
RUN mkdir -p /app/static
RUN python manage.py collectstatic --no-input  
EXPOSE 8000
CMD ["gunicorn", "ArtUs.wsgi:application", "--bind", "0.0.0.0:8000"]
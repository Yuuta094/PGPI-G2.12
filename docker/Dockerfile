FROM python:3.10-alpine

WORKDIR /app/
# Install Git
RUN apk add --no-cache git

RUN git clone https://github.com/Yuuta094/PGPI-G2.12.git PGPI-G2.12

WORKDIR /app/PGPI-G2.12/artus
ENV PYTHONPATH /app/PGPI-G2.12/artus/artus
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "artus.wsgi:application", "--bind", "0.0.0.0:8000"]
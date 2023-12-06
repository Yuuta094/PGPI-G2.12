
FROM python:3.10-alpine
RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app


RUN git clone https://github.com/Yuuta094/PGPI-G2.12.git 

WORKDIR /app/PGPI-G2.12\artUS\
RUN pip install -r requirements.txt

COPY settings.py /app/artUS/artus/settings.py


EXPOSE 8000
CMD ["gunicorn", "artUS.artus.wsgi:application", "--bind", "0.0.0.0:8000"]



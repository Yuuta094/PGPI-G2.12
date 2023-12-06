
FROM python:3.10.11


WORKDIR /app


RUN git clone https://github.comcd P/Yuuta094/PGPI-G2.12.git 

WORKDIR /app/PGPI-G2.12/artUS





# Instalar  dependencias
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn


RUN python manage.py makemigrations
RUN python manage.py migrate




EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "artus.artus.wsgi:application", "--bind", "0.0.0.0:8000"]
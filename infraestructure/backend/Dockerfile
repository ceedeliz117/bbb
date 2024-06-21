# Usa una imagen base de Python
FROM python:3.9-slim

RUN apt-get update && apt-get install -y sqlite3

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos a la imagen
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto al directorio de trabajo
COPY backend/api /app

# Expone el puerto en el que correrá la app
EXPOSE 8000

# Corre las migraciones y lanza el servidor de desarrollo de Django
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

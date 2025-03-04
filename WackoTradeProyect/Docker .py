# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos y lo instalamos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de la aplicación al contenedor
COPY . .

# Definimos el comando que se ejecutará al iniciar el contenedor
CMD ["python", "main.py"]

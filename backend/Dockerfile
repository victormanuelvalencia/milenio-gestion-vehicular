# Imagen base con Python
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el backend
COPY . .

# Puerto donde escuchará FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación
CMD [
  "uvicorn",
  "app.main:app",
  "--host","0.0.0.0",
  "--port","8000",
  "--proxy-headers",
  "--forwarded-allow-ips=*"
]
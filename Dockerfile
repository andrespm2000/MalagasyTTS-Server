# Usa una imagen base de Python
FROM python:3.12.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .
COPY main.py .
COPY detection.py .
COPY translation.py .
COPY narration.py .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Comando que se ejecutará cuando el contenedor inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Dockerfile explicado

Este archivo describe el `Dockerfile` que está en la raíz del proyecto. El `Dockerfile` define cómo construir la imagen de Docker que ejecuta la aplicación Django.

## Por qué hay dos etapas

El Dockerfile usa dos etapas:

1. **Etapa de compilación** (`build stage`): instala paquetes, crea el entorno virtual y prepara todo lo necesario.
2. **Etapa de ejecución** (`runtime stage`): usa una imagen limpia y copia solo lo necesario para que la aplicación corra.

Esto se hace para que la imagen final sea más pequeña y más eficiente.

## Etapa de compilación

```dockerfile
FROM python:3.13-slim AS builder
```
- Usa una imagen ligera de Python 3.13.
- `AS builder` le da un nombre a esta etapa para copiar cosas después.

```dockerfile
RUN pip install --no-cache-dir uv
```
- Instala `uv`, una herramienta para crear entornos virtuales y administrar dependencias.
- `--no-cache-dir` evita guardar archivos temporales de descarga.

```dockerfile
WORKDIR /app
```
- Cambia la carpeta de trabajo a `/app`.
- Todas las instrucciones siguientes se ejecutan desde allí.

```dockerfile
COPY pyproject.toml uv.lock* ./
```
- Copia los archivos que dicen qué dependencias necesita el proyecto.
- Esto permite instalar las librerías necesarias sin copiar todo el código primero.

```dockerfile
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python -e .
```
- Crea un entorno virtual en `/opt/venv`.
- Instala las dependencias del proyecto en ese entorno.
- `-e .` instala el proyecto en modo editable para que el código esté disponible dentro del contenedor.

## Etapa de ejecución

```dockerfile
FROM python:3.13-slim
```
- Parte de una imagen limpia para ejecutar la aplicación.
- No incluye las herramientas de compilación de la primera etapa.

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*
```
- Instala `libpq5`, que necesita `psycopg2-binary` para conectarse a PostgreSQL.
- `--no-install-recommends` evita instalar paquetes adicionales innecesarios.
- Se limpia la caché de instalación para reducir el tamaño de la imagen.

```dockerfile
COPY --from=builder /opt/venv /opt/venv
```
- Copia el entorno virtual ya instalado desde la etapa de compilación.
- Así no es necesario reinstalar las dependencias.

```dockerfile
WORKDIR /app
```
- Establece de nuevo la carpeta de trabajo en la etapa de ejecución.

```dockerfile
COPY . .
```
- Copia el código de la aplicación dentro del contenedor.
- Incluye archivos Django, configuraciones y demás código del proyecto.

```dockerfile
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
```
- Añade el entorno virtual al `PATH` para usar Python y paquetes instalados allí.
- `PYTHONUNBUFFERED=1` hace que Python escriba los logs inmediatamente.
- `PYTHONDONTWRITEBYTECODE=1` evita crear archivos `.pyc`.

```dockerfile
EXPOSE 8000
```
- Indica que el contenedor escucha en el puerto `8000`.
- Este es el puerto donde se ejecuta la aplicación Django.

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')"
```
- Agrega un chequeo de salud para que Docker sepa si la aplicación está funcionando.
- Cada 30 segundos intenta acceder a `http://localhost:8000/health/`.
- Si la app no responde, el contenedor se marca como no saludable.

## Resumen

- La primera etapa prepara el entorno y las dependencias.
- La segunda etapa crea una imagen más ligera con solo lo necesario para ejecutar la app.
- Esto ayuda a que el contenedor sea más pequeño y más fácil de usar.

# ================ STAGE 1: Build dependencies (con cache eterno) ================
FROM python:3.14-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1
    # Ya no necesitas PYTHONUNBUFFERED en build

WORKDIR /app

# Instala solo las dependencias del sistema necesarias para mysqlclient
# Usamos --mount=type=cache para que apt cachee para siempre
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia solo lo necesario para instalar dependencias de Python
COPY requirements.txt .
# Aquí también cacheamos pip para que nunca más baje paquetes si no cambian
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# ================ STAGE 2: Runtime (livianito y sin basura) ================
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Solo copiamos las librerías de sistema que realmente necesita mysqlclient en runtime
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiamos Python + paquetes del stage anterior
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Resto de tu app
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
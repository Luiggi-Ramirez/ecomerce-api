#!/bin/bash
echo instalando mysql drivers && \
    apt-get update && apt-get install -y \
    gnupg2 \
    unixodbc-dev \
    build-essential \
    pkg-config \
    mariadb-client \
    libmariadb-dev-compat && \
    apt-get clean && \
    pip install --no-cache-dir mysqlclient && \
    echo mysql drivers instalados; \
python manage.py runserver 0.0.0.0:8000
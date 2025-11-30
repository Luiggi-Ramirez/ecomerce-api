FROM python:3.14-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

COPY . /app/

EXPOSE 8000

CMD [ "/usr/local/bin/entrypoint.sh" ]

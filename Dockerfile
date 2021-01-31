FROM python:3.7.9

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    useradd -M app
COPY src/ .
COPY key.json /credentials/
USER app
ENV GOOGLE_APPLICATION_CREDENTIALS=/credentials/key.json

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
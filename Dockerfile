FROM python:3.7.9-alpine3.12

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    adduser -D app
COPY src/ .
USER app
EXPOSE 80

ENTRYPOINT python app.py
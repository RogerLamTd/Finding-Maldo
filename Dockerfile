FROM python:3.7.9

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    useradd -M app
COPY src/ .
COPY key.json /credentials/
USER app
EXPOSE 80
ENV GOOGLE_APPLICATION_CREDENTIALS=/credentials/key.json

ENTRYPOINT ["python", "app.py"]
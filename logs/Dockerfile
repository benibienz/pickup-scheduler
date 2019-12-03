FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir pika
COPY recieve_logs.py .
CMD [ "python", "./recieve_logs.py" ]
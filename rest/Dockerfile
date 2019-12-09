FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir pika flask redis pandas
COPY rest-server.py .
CMD [ "python", "./rest-server.py" ]
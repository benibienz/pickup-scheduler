FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir pika redis pandas
COPY game-scheduler.py .
CMD [ "python", "./game-scheduler.py" ]
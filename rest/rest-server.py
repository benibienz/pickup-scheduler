#!/usr/bin/env python3
from flask import Flask, request, Response
import redis
import pickle
import pika

APP = Flask(__name__)


@APP.route('/facility/<name>', methods=['PUT'])
def new_facility_calendar(name):
    try:
        send_message(msg=f'REST server received new facility: {name}', exchange='logs', key='info')
        facilitiesdb.set(name, request.data)
        return Response(response=f'New facility calendar: {name}', status=200)

    except Exception as e:
        # send debug msg
        send_message(msg=f'REST server exception: {e}', exchange='logs', key='debug')
        return Response(response=e, status=500)


@APP.route('/player/<name>', methods=['PUT'])
def match_player(name):
    try:
        send_message(msg=f'REST server received player match request for {name}', exchange='logs', key='info')
        send_message(msg=request.data, exchange='toGS')
        return Response(response=f'Matching player: {name}', status=200)

    except Exception as e:
        # send debug msg
        send_message(msg=f'REST server exception: {e}', exchange='logs', key='debug')
        return Response(response=e, status=500)


# @APP.route('/???/<checksum>', methods=['GET'])
# def get_something(something):
#     send_message(msg=f'REST server received GET request for {something}', exchange='logs', key='info')
#     return Response(response=redisByChecksum.get(something), status=200)


def send_message(msg, exchange, key=None):
    """
    Sends message to RabbitMQ exchange
    Args:
        msg: message content
        exchange: 'logs' or 'toWorker'
        key: optional key 'debug' or 'info' for logs exchange only
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    exchange_type = 'direct' if exchange == 'toGS' else 'topic'
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    if key is not None and exchange == 'logs':
        routing_key = f'rest.{key}'
    else:
        routing_key = ''
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
    connection.close()


if __name__ == '__main__':
    # Connect to redis databases
    gamesdb = redis.Redis(host='redis', db=1)
    facilitiesdb = redis.Redis(host='redis', db=2)
    playersdb = redis.Redis(host='redis', db=3)

    # run flask app
    APP.run(host='0.0.0.0', port=5000)

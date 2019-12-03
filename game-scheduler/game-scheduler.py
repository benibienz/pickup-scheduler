#!/usr/bin/env python3
import pika
import pickle
import redis


def callback(ch, method, properties, body):
    """ RabbitMQ callback """
    player_cal = pickle.loads(body)
    send_message(f'Received calendar for {player_cal.name}', exchange='logs', key='info')

    try:
        # get FM calendar
        # TODO: scale??
        fm_cal = pickle.loads(facilitiesdb.get('FM'))
        filled_teams = fm_cal.match_with_player(player_cal)
    except Exception as e:
        filled_teams = []
        send_message(f'Error getting FM calendar {e}', exchange='logs', key='debug')

    for team in filled_teams:
        send_message(f'Team filled at {team}', exchange='logs', key='info')
        send_message(pickle.dumps(fm_cal.get_team(team)), exchange='toES')

    # update FM db
    facilitiesdb.set('FM', pickle.dumps(fm_cal))

    # acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_message(msg, exchange, key=None):
    """
    Sends message to RabbitMQ exchange
    Args:
        msg: message content
        exchange: 'logs' or 'toES'
        key: optional key 'debug' or 'info' for logs exchange only
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    exchange_type = 'direct' if exchange == 'toES' else 'topic'
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    if key is not None and exchange == 'logs':
        routing_key = f'scheduler.{key}'
    else:
        routing_key = ''
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
    connection.close()


def main():
    worker_channel = RABBITMQ_CONNECTION.channel()
    worker_channel.exchange_declare(exchange='toGS', exchange_type='direct')
    result = worker_channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    worker_channel.queue_bind(exchange='toGS', queue=queue_name, routing_key='')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    worker_channel.basic_consume(queue=queue_name, on_message_callback=callback)
    worker_channel.start_consuming()


if __name__ == '__main__':
    # Connect to redis databases
    gamesdb = redis.Redis(host='redis', db=1)
    facilitiesdb = redis.Redis(host='redis', db=2)
    playersdb = redis.Redis(host='redis', db=3)
    RABBITMQ_CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    THIS_ADDR = 'game-scheduler'
    main()


#!/usr/bin/env python3
import pika


def callback(ch, method, properties, body):
    txt = '[x] {}: {}'.format(method.routing_key, body)
    print(txt, flush=True)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=LOGS_SERVER))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = ['*.debug', '*.info']
    for binding_key in binding_keys:
        channel.queue_bind(exchange='logs', queue=queue_name, routing_key=binding_key)

    txt = ' [*] Waiting for logs. To exit press CTRL+C'
    print(txt, flush=True)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    LOGS_SERVER = 'rabbitmq'
    main()

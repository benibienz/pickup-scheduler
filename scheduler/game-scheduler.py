#!/usr/bin/env python3
import pika
import pickle
import redis
import random
import pandas
from collections import defaultdict


class FacilityCalendar:
    def __init__(self, price_cal, max_players=2):
        self.max_players = max_players
        self.price_cal = price_cal
        self.team_cal = price_cal.copy() * 0
        self.team_dict = defaultdict(list)

    def match_with_player(self, name, player_cal):
        updated_team_cal = self.team_cal.copy()
        filled_team_keys = []
        for loc in player_cal.stack().index:
            current_player_count = self.team_cal.at[loc]
            if self.price_cal.at[loc] <= player_cal.at[loc]:
                if current_player_count < self.max_players:
                    updated_team_cal.at[loc] += 1
                    self.team_dict[f'{loc[1]}-{loc[0]}'].append(name)
                    if current_player_count == self.max_players - 1:
                        filled_team_keys.append(f'{loc[1]}-{loc[0]}')
                else:
                    continue  # team is filled

        self.team_cal = updated_team_cal
        return filled_team_keys

    def get_team(self, key):
        return self.team_dict[key]


def make_teams(players):
    """ Random selection for now """
    team_size = int(len(players) / 2)
    random.shuffle(players)
    return players[:team_size], players[team_size:]


def callback(ch, method, properties, body):
    """ RabbitMQ callback """
    name = body
    player_cal = pickle.loads(playersdb.get(name))
    send_message(f'Received calendar for {name}', exchange='logs', key='info')

    try:
        # get FM calendar
        # TODO: scale??
        fm_cal = pickle.loads(facilitiesdb.get('FM'))
        filled_games = fm_cal.match_with_player(name, player_cal)
    except Exception as e:
        send_message(f'Error getting FM calendar {e}', exchange='logs', key='debug')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    for timeslot in filled_games:
        send_message(f'Game filled at {timeslot}', exchange='logs', key='info')
        player_list = fm_cal.get_team(timeslot)

        send_message(f'Player list: {player_list}', exchange='logs', key='debug')
        send_message(f'Team dict: {fm_cal.team_dict}', exchange='logs', key='debug')

        # assign teams
        team_a, team_b = make_teams(player_list)

        # create game object and set db
        game = {'team A': team_a, 'team B': team_b, 'result': None}
        gamesdb.set(timeslot, pickle.dumps(game))
        send_message(f'Game created at {timeslot}', exchange='logs', key='info')

    # update FM db
    facilitiesdb.set('FM', pickle.dumps(fm_cal))

    # acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_message(msg, exchange, key=None):
    """
    Sends message to RabbitMQ exchange
    Args:
        msg: message content
        exchange: 'logs'
        key: optional key 'debug' or 'info' for logs exchange only
    """
    print(msg)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    exchange_type = 'direct' if exchange == 'other' else 'topic'
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
    main()


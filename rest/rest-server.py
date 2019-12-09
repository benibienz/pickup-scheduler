#!/usr/bin/env python3
from flask import Flask, request, Response
import redis
import pickle
import pika
import pandas

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


@APP.route('/match/<name>', methods=['PUT'])
def match_player(name):
    try:
        send_message(msg=f'REST server received player match request for {name}', exchange='logs', key='info')
        cal = pickle.loads(request.data)
        if playersdb.exists(name):
            player = pickle.loads(playersdb.get(name))
            if player['calendar'] is not None:
                # cannot submit new calendar
                return Response(response=f'Player already matched: {name}\n', status=200)
        else:
            player = {'calendar': None, 'games': [], 'score': 0}
        player['calendar'] = cal
        playersdb.set(name, pickle.dumps(player))
        send_message(msg=name, exchange='toGS')
        return Response(response=f'Matching player: {name}', status=200)

    except Exception as e:
        # send debug msg
        send_message(msg=f'REST server exception: {e}', exchange='logs', key='debug')
        return Response(response=e, status=500)


@APP.route('/player/<name>', methods=['GET'])
def get_player_info(name):
    send_message(msg=f'REST server received player info request for {name}', exchange='logs', key='info')
    player = pickle.loads(playersdb.get(name))
    resp = f"Info for player {name}:\nGames: {player['games']}\nScore: {player['score']}\n"
    return Response(response=resp, status=200)


@APP.route('/game/<key>', methods=['GET'])
def get_game_info(key):
    send_message(msg=f'REST server received game info request for {key}', exchange='logs', key='info')
    game = pickle.loads(gamesdb.get(key))
    resp = f"Info for game on {key}:\nTeam A: {game['team A']}\nTeam B: {game['team B']}\n" \
           f"Winner: {game['result']}\n"
    return Response(response=resp, status=200)


@APP.route('/report/<key>/<res>', methods=['PUT'])
def report_game_result(key, res):
    send_message(msg=f'REST server received game result for {key}', exchange='logs', key='info')
    if not gamesdb.exists(key):
        return Response(response=f'game does not exist', status=200)
    game = pickle.loads(gamesdb.get(key))
    if game['result'] is not None:
        # already reported
        return Response(response=f'Game already reported as {game["result"]}', status=200)
    else:
        # add scores to players
        for team in ['A', 'B']:
            for name in game[f'team {team}']:
                player = pickle.loads(playersdb.get(name))
                if res == team:
                    player['score'] += 3  # 3 for a win
                elif res == 'tie':
                    player['score'] += 1  # 1 for a tie
                playersdb.set(name, pickle.dumps(player))

        # record result
        game['result'] = res
        gamesdb.set(key, pickle.dumps(game))
        return Response(response=f'Game at {key} result: {res} - saved\n', status=200)


@APP.route('/new', methods=['PUT'])
def new_week():
    """ Start a new week """
    gamesdb.flushdb()  # flush games
    facilitiesdb.flushdb()  # flush facilities

    # reset player games and calendars but keep scores
    for name in playersdb.keys():
        player = pickle.loads(playersdb.get(name))
        player['calendar'] = None
        player['games'] = []
        playersdb.set(name, pickle.dumps(player))
    send_message('New week request received', exchange='logs', key='info')
    return Response(response='DBs flushed. New week begins\n', status=200)


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

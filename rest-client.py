#!/usr/bin/env python3
import argparse
import requests
import json
import pathlib
import pickle
import pandas as pd

from calendars import FacilityCalendar

DATAPATH = pathlib.Path(__file__).parents[0].joinpath('data')


def send_facility_calendar(name, addr):
    url = f'{addr}/facility/{name}'
    price_cal = pd.read_csv(DATAPATH.joinpath(name + '.csv'), index_col=0)
    price_cal.name = name
    cal = FacilityCalendar(price_cal)

    # send http request and receive response
    response = requests.put(url, data=pickle.dumps(cal))

    # decode response
    print('Response code: {}'.format(response.status_code))
    if response.status_code == 200:
        print(json.loads(response.text))


def send_player_calendar(name, addr):
    url = f'{addr}/player/{name}'
    cal = pd.read_csv(DATAPATH.joinpath(name + '.csv'), index_col=0)
    cal.name = name

    # send http request and receive response
    response = requests.put(url, data=pickle.dumps(cal))

    # decode response
    print('Response code: {}'.format(response.status_code))
    if response.status_code == 200:
        print(json.loads(response.text))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host')
    parser.add_argument('--name', help='Player name')
    args = parser.parse_args()

    send_player_calendar(name=args.name, addr=f'http://{args.host}:5000')

#!/usr/bin/env python3
import argparse
import requests
import json
import pathlib
import pickle
import pandas as pd
from collections import defaultdict

DATAPATH = pathlib.Path(__file__).parents[0].joinpath('data')


class FacilityCalendar:
    def __init__(self, price_cal, team_size):
        self.team_size = team_size
        self.price_cal = price_cal
        self.team_cal = price_cal.copy() * 0
        self.team_dict = defaultdict(list)

    def match_with_player(self, name, player_cal):
        updated_team_cal = self.team_cal.copy()
        filled_team_keys = []

        for loc in player_cal.stack().index:
            current_player_count = self.team_cal.at[loc]
            if self.price_cal.at[loc] <= player_cal.at[loc]:
                if current_player_count < self.team_size * 2:
                    updated_team_cal.at[loc] += 1
                    self.team_dict[f'{loc[1]}-{loc[0]}'].append(name)
                    if current_player_count == self.team_size * 2 - 1:
                        filled_team_keys.append(f'{loc[1]}-{loc[0]}')
                else:
                    continue  # team is filled

        self.team_cal = updated_team_cal
        return filled_team_keys

    def get_team(self, key):
        return self.team_dict[key]


def send_facility_calendar(name, addr, team_size):
    url = f'{addr}/facility/{name}'
    price_cal = pd.read_csv(DATAPATH.joinpath(name + '.csv'), index_col=0)
    cal = FacilityCalendar(price_cal, team_size=team_size)

    # send http request and receive response
    response = requests.put(url, data=pickle.dumps(cal))

    # decode response
    print(response.text)


def send_player_calendar(name, addr):
    url = f'{addr}/match/{name}'
    cal = pd.read_csv(DATAPATH.joinpath(name + '.csv'), index_col=0)

    # send http request and receive response
    response = requests.put(url, data=pickle.dumps(cal))

    # decode response
    print(response.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host')
    parser.add_argument('--user', default='player', help='"player" or "fm"')
    parser.add_argument('--teamsize', default=None, help='team size for FM cal')
    parser.add_argument('--name', help='Player or facility name')

    args = parser.parse_args()

    if args.user == 'player':
        send_player_calendar(name=args.name, addr=f'http://{args.host}:5000')
    else:
        send_facility_calendar(name=args.name,
                               addr=f'http://{args.host}:5000',
                               team_size=int(args.teamsize))

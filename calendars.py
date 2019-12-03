#!/usr/bin/env python3
import pandas as pd
import pathlib
import numpy as np
import pickle
from collections import defaultdict

DATAPATH = pathlib.Path(__file__).parents[0].joinpath('data')


class FacilityCalendar:
    def __init__(self, price_cal, max_players=2):
        self.max_players = max_players
        self.price_cal = price_cal
        self.team_cal = price_cal.copy() * 0
        self.team_dict = defaultdict(list)

    def match_with_player(self, player_cal):
        updated_team_cal = self.team_cal.copy()
        filled_team_keys = []
        for loc in player_cal.stack().index:
            current_player_count = self.team_cal.at[loc]
            if self.price_cal.at[loc] <= player_cal.at[loc]:
                if current_player_count < self.max_players:
                    updated_team_cal.at[loc] += 1
                    self.team_dict[f'{loc[1]}-{loc[0]}'].append(player_cal.name)
                    if current_player_count == self.max_players - 1:
                        filled_team_keys.append(f'{loc[1]}-{loc[0]}')
                else:
                    continue  # team is filled

        self.team_cal = updated_team_cal
        return filled_team_keys

    def get_team(self, key):
        return self.team_dict[key]


def fm_create_blank_calendar(name, price=5, open=7, close=23):
    idx = pd.Index(range(0, 24), name='Hour')
    cols = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday']
    cal = pd.DataFrame(index=idx, columns=cols)
    for day in cols:
        cal.loc[open:close - 1, day] = price
    cal.name = name
    cal.to_csv(DATAPATH.joinpath(name + '.csv'))


def player_create_blank_calendar(avail_hours, name, price_limit=5):
    idx = pd.Index(range(0, 24), name='Hour')
    cols = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday']
    cal = pd.DataFrame(index=idx, columns=cols)
    for day in cols:
        cal.loc[avail_hours, day] = price_limit
    cal.name = name
    cal.to_csv(DATAPATH.joinpath(name + '.csv'))


if __name__ == '__main__':
    # fm_create_blank_calendar('FM')
    # player_create_blank_calendar(avail_hours=[20, 21], name='Bob')
    FC = FacilityCalendar(pd.read_csv(DATAPATH.joinpath('FM.csv'), index_col=0))
    alice = pd.read_csv(DATAPATH.joinpath('Alice.csv'), index_col=0)
    alice.name = 'Alice'
    FC.match_with_player(alice)
    bob = pd.read_csv(DATAPATH.joinpath('Bob.csv'), index_col=0)
    bob.name = 'Bob'
    FC.match_with_player(bob)


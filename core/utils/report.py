import constants
import json
import os

data = {}

def store(key, value):
    data[key] = value

def store_time(key, time_in_seconds):
    data[key] = "{:.3f} seconds".format(time_in_seconds)

def dump():
    path = os.path.join(constants.workspace,'report.json')

    with open(path, 'w') as f:
        json.dump(data, f)
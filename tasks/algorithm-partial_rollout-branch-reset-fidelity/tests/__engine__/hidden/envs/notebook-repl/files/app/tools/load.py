import json

data = json.load(open('data/readings.json'))


def above(th):
    return [d['t'] for d in data if d['v'] > th]

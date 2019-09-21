import json


def read_json(path):
    with open(path) as f:
        return json.load(f)


def read_file(path):
    with open(path) as f:
        return f.read()

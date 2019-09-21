import json

from src.handler import parse


def read_json(path):
    with open(path) as f:
        return json.load(f)


def read_file(path):
    with open(path) as f:
        return f.read()


def test_parse():
    input = read_json('tests/resources/response.json')
    true_output = read_file('tests/resources/true_output.xml')

    out = parse(input)
    atom_str = out.atom_str(pretty=True).decode('utf-8')
    assert atom_str == true_output

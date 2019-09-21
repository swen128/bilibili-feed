import requests_mock

from src.handler import endpoint
from tests.utils import read_file

bilibili_api_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'


def test_valid_request():
    uid = '436596841'
    event = {'queryStringParameters': {'uid': uid}}
    true_output = read_file('tests/resources/true_output.xml')
    bilibili_response = read_file('tests/resources/response.json')

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, text=bilibili_response)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=200,
        body=true_output
    )


def test_invalid_request():
    response = endpoint(event={}, context={})

    assert response == dict(
        statusCode=400,
        body='bilibili user ID is not specified.'
    )


def test_empty_bilibili_response():
    uid = 'place holder'
    event = {'queryStringParameters': {'uid': uid}}
    bilibili_response = read_file('tests/resources/empty_response.json')

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, text=bilibili_response)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=403,
        body='The specified bilibili user ID was not found.'
    )


def test_unknown_bilibili_respone():
    uid = '436596841'
    event = {'queryStringParameters': {'uid': uid}}
    bilibili_response = read_file('tests/resources/unknown_response.json')

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, text=bilibili_response)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=500,
        body='Internal server error.'
    )

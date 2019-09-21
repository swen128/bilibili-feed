import requests_mock

from src.handler import endpoint
from tests.utils import read_file

bilibili_api_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'


def test_valid_request_0():
    uid = '436596841'
    event = {'queryStringParameters': {'uid': uid}}
    true_output = read_file('tests/resources/atom_feed/valid_0.xml')
    bilibili_response = read_file('tests/resources/bilibili_api_response/valid_0.json')

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, text=bilibili_response)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=200,
        body=true_output
    )


def test_valid_request_1():
    uid = '410455162'
    event = {'queryStringParameters': {'uid': uid}}
    true_output = read_file('tests/resources/atom_feed/valid_1.xml')
    bilibili_response = read_file('tests/resources/bilibili_api_response/valid_1.json')

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
    bilibili_response = read_file('tests/resources/bilibili_api_response/empty.json')

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
    bilibili_response = read_file('tests/resources/bilibili_api_response/unknown_format.json')

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, text=bilibili_response)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=500,
        body='Internal server error.'
    )


def test_partially_unknown_bilibili_response():
    uid = '436596841'
    event = {'queryStringParameters': {'uid': uid}}
    true_output = read_file('tests/resources/atom_feed/partially_unknown_format.xml')
    bilibili_response = read_file('tests/resources/bilibili_api_response/partially_unknown_format.json')

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, text=bilibili_response)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=200,
        body=true_output
    )


def test_request_exception():
    uid = '436596841'
    event = {'queryStringParameters': {'uid': uid}}

    with requests_mock.Mocker() as m:
        m.get(bilibili_api_url, status_code=500)

        response = endpoint(event, context={})

    assert response == dict(
        statusCode=503,
        body='The server could not connect to the bilibili dynamic API.'
    )

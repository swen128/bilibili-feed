import requests

from requests.exceptions import RequestException

from src.parser import \
    parse_bilibili_dynamic_to_feed, \
    BilibiliUnknownResponseException, \
    BilibiliEmptyResponseException


def endpoint(event: dict, context: dict) -> dict:
    try:
        host_uid = event['queryStringParameters']['uid']
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'bilibili user ID is not specified.'
        }

    try:
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
        bilibili_response = requests.get(url, params={'host_uid': host_uid})

        bilibili_response.raise_for_status()
    except RequestException:
        return {
            "statusCode": 503,
            "body": 'The server could not connect to the bilibili dynamic API.'
        }

    try:
        feed = parse_bilibili_dynamic_to_feed(bilibili_response.json())
        return {
            "statusCode": 200,
            "body": feed
        }
    except BilibiliUnknownResponseException:
        return {
            "statusCode": 500,
            "body": 'Internal server error.'
        }
    except BilibiliEmptyResponseException:
        return {
            "statusCode": 403,
            "body": 'The specified bilibili user ID was not found.'
        }

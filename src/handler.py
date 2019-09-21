import requests
from src.parser import parse_bilibili_dynamic_to_feed


def endpoint(event: dict, context: dict) -> dict:
    try:
        host_uid = event['queryStringParameters']['uid']
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'bilibili user ID is not specified.'
        }

    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
    bilibili_response = requests.get(url, params={'host_uid': host_uid})

    feed = parse_bilibili_dynamic_to_feed(bilibili_response.json())
    body = feed.atom_str(pretty=True).decode('utf-8')

    response = {
        "statusCode": 200,
        "body": body
    }

    return response

import json
from datetime import datetime, timezone

from feedgen.feed import FeedGenerator


def parse_bilibili_dynamic_to_feed(response: dict) -> FeedGenerator:
    cards = response['data']['cards']
    desc = cards[0]['desc']
    user_name = desc['user_profile']['info']['uname']
    last_updated = datetime.fromtimestamp(desc['timestamp'], tz=timezone.utc)
    user_id = desc['uid']
    feed_title = f'{user_name} - bilibili dynamic'
    dynamic_url = f'https://space.bilibili.com/{user_id}/dynamic'

    feed = FeedGenerator()
    feed.id(dynamic_url)
    feed.link(href=dynamic_url, rel='alternate')
    feed.title(feed_title)
    feed.updated(last_updated)
    feed.language('cn')

    for card in cards:
        desc = card['desc']
        dynamic_id = str(desc['dynamic_id'])
        timestamp = datetime.fromtimestamp(desc['timestamp'], tz=timezone.utc)

        link = f'https://t.bilibili.com/{dynamic_id}'
        card_dic = json.loads(card['card'])

        entry = feed.add_entry()

        if 'aid' in card_dic:
            aid = card_dic['aid']
            title = card_dic['title']
            thumbnail = card_dic['pic']
            video_url = f'https://www.bilibili.com/video/av{aid}'
            content = ''

            entry.link(href=video_url, rel='enclosure')
        elif 'item' in card_dic:
            title = feed_title
            item = card_dic['item']
            content = item['content']
            thumbnail = card_dic['user']['face']

            if 'origin' in card_dic:
                origin_id = card_dic['item']['orig_dy_id']
                origin_url = f'https://t.bilibili.com/{origin_id}'
                content += f'\n\nin reply to: {origin_url}'

        else:
            raise ValueError()

        entry.id(dynamic_id)
        entry.link(href=link, rel='alternate', type='text/html')
        entry.link(href=thumbnail, rel='enclosure', type='image/jpeg')
        entry.title(title)
        entry.content(content)
        entry.updated(timestamp)

    return feed

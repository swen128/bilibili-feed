import json
from datetime import datetime, timezone

from feedgen.feed import FeedGenerator, FeedEntry


class BilibiliEmptyResponseException(Exception):
    pass


class BilibiliUnknownResponseException(Exception):
    pass


def parse_card_to_entry(card: dict) -> FeedEntry:
    entry = FeedEntry()

    desc = card['desc']
    dynamic_id = str(desc['dynamic_id'])
    timestamp = datetime.fromtimestamp(desc['timestamp'], tz=timezone.utc)

    link = f'https://t.bilibili.com/{dynamic_id}'
    card_dic = json.loads(card['card'])

    if 'aid' in card_dic:
        aid = card_dic['aid']
        title = card_dic['title']
        thumbnail = card_dic['pic']
        video_url = f'https://www.bilibili.com/video/av{aid}'
        content = video_url

        entry.link(href=video_url, rel='related')
    elif 'item' in card_dic:
        user_name = desc['user_profile']['info']['uname']
        title = f'post from {user_name}'
        item = card_dic['item']

        if 'pictures' in item:
            content = item['description']
            thumbnail = item['pictures'][0]['img_src']
        elif 'video_playurl' in item:
            content = item['description']
            cover = item['cover']
            thumbnail = cover.get('unclipped') or cover['default']
        elif 'origin' in card_dic:
            origin_id = card_dic['item']['orig_dy_id']
            origin_url = f'https://t.bilibili.com/{origin_id}'
            reply_text = item['content']
            content = f'{reply_text}\n\nin reply to: {origin_url}'
            thumbnail = card_dic['user']['face']
        else:
            content = item['content']
            thumbnail = card_dic['user']['face']
    else:
        raise ValueError()

    entry.id(dynamic_id)
    entry.link(href=link, rel='alternate', type='text/html')
    entry.link(href=thumbnail, rel='enclosure', type='image/jpeg')
    entry.title(title)
    entry.content(content)
    entry.updated(timestamp)

    return entry


def parse_bilibili_dynamic_to_feed(response: dict) -> str:
    if not response.get('data', {}).get('cards'):
        raise BilibiliEmptyResponseException()

    try:
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
    except:
        raise BilibiliUnknownResponseException()

    for card in cards:
        entry = parse_card_to_entry(card)
        feed.add_entry(feedEntry=entry)

    try:
        atom_str = feed.atom_str(pretty=True).decode('utf-8')
        return atom_str
    except:
        raise BilibiliUnknownResponseException()

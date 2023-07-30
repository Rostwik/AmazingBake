from urllib.parse import urlparse

import requests


def get_short_link(token, target_url):
    """Возвращает короткую ссылку из сервиса Bitly"""
    headers = {
        'Authorization': f'Bearer {token}',
    }
    bitly_url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {
        'long_url': target_url,
    }
    response = requests.post(bitly_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def get_count_clicks(token, short_link, unit='day'):
    """Возвращает количество кликов по короткой ссылке за весь период"""
    link_parts = urlparse(short_link)
    bitlink = f'{link_parts.netloc}{link_parts.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = (
        ('unit', unit),
        ('units', '1'),
    )
    response = requests.get(url=url, headers=headers, params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    """Возвращает True или False проверки битлинка"""
    headers = {
        'Authorization': f'Bearer {token}',
    }
    link_parts = urlparse(url)
    bitlink_id = f'{link_parts.netloc}{link_parts.path}'
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}'
    response = requests.get(bitly_url, headers=headers)
    return response.ok

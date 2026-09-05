from random import choice
from string import ascii_lowercase

import requests

from helpers.base import BaseURL


def generate_random_string(length=10):
    """Генерирует случайную строку из строчных букв."""
    letters = ascii_lowercase
    return "".join(choice(letters) for _ in range(length))


def generate_unique_email():
    """Генерирует уникальный email."""
    return f"{generate_random_string()}@example.com"


def get(url, headers=None):
    return requests.get(url, headers=headers).json()


def post(url, json, headers=None):
    return requests.post(
        url,
        json=json,
        headers=headers,
    ).json()


def patch(url, json, headers=None):
    return requests.patch(
        url,
        json=json,
        headers=headers,
    ).json()


def delete(url):
    return requests.delete(url)

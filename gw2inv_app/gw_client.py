# -*- coding: utf-8 -*-
import time
import typing

import requests
from django.conf import settings

from .dto import *

API_BASE_URL = "https://api.guildwars2.com/"


class Client:
    def __init__(self):
        self._api_base_url = API_BASE_URL
        self._last_fetch = 0
        self._time_between_fetch_seconds = 1

    def _make_args(self, api: str) -> typing.Dict[str, str]:
        key = settings.GW2_API_KEY
        return {
            "url": f"{self._api_base_url}{api}",
            "headers": {
                "Authorization": f"Bearer {key}",
                "X-Schema-Version": "latest",  # TODO: Sticky this later
            },
        }

    def _get(self, path: str):
        sleep_time = self._last_fetch + self._time_between_fetch_seconds - time.time()
        if sleep_time > 0:
            print("Sleeping", sleep_time, end="")
            time.sleep(sleep_time)
            print("\r", " " * 64, "\r", end="")

        print("GET", path)
        response = requests.get(**self._make_args(path))
        print(
            "<-",
            response.status_code,
            ", content-length:",
            response.headers.get("content-length"),
        )
        response.raise_for_status()
        self._last_fetch = time.time()
        return response.json()

    def get_characters(self) -> typing.List[str]:
        return self._get("v2/characters")

    def get_character_core(self, character_id: str):
        data = self._get("v2/characters/" + character_id + "/core")
        obj = CoreSchema().load(data, unknown="EXCLUDE")
        return obj

    def get_character_equipment(self, character_id: str):
        data = self._get("v2/characters/" + character_id + "/equipment")
        obj = EquipmentResponseSchema().load(data, unknown="EXCLUDE")
        return obj

    def get_character_inventory(self, character_id: str):
        data = self._get("v2/characters/" + character_id + "/inventory")
        obj = InventoryResponseSchema().load(data, unknown="EXCLUDE")
        return obj

    def get_item(self, item_id: int):
        data = self._get("v2/item/" + str(item_id))
        obj = ItemSchema().load(data, unknown="EXCLUDE")
        return obj

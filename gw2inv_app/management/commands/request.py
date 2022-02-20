# -*- coding: utf-8 -*-

import json
import os
import typing

import marshmallow
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from gw2inv_app import dto

TYPES = {
    "bank": dto.BankSchema,
    "character": dto.CharacterSchema,
    "item": dto.ItemSchema,
    "equipment": dto.EquipmentResponseSchema,
    "inventory": dto.InventoryResponseSchema,
}


class Command(BaseCommand):
    help = "Do a request to GW2 API."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            "--get",
            "-g",
            type=str,
            metavar="PATH",
            help="Do API GET request. PATH must start with v2/",
        )
        parser.add_argument(
            "--load",
            "-l",
            type=str,
            metavar="FILE_PATH",
            help="Deserialize cached json file and print python repr of it.",
        )
        parser.add_argument(
            "--type",
            "-t",
            type=str,
            metavar="DTO_TYPE",
            choices=TYPES.keys(),
            help="Deserialize with DTO: {}. If not given, prints python repr.".format(
                ", ".join(TYPES.keys())
            ),
        )
        parser.add_argument(
            "--multi",
            "-m",
            action="store_true",
            default=False,
            help="Is the response a list? Affects only --type",
        )
        parser.add_argument(
            "--items",
            action="store_true",
            default=False,
            help="Parse item id:s from character (FLAKY).",
        )

    def print(self, *args, **kwargs):
        print(*args, **kwargs, file=self.stdout)

    def handle(self, *args, **options):
        dtype = TYPES.get(options["type"].lower()) if options["type"] else None

        if options["get"]:
            self._get(options["get"], dtype, options)
        elif options["load"]:
            self._load(options["load"], dtype, options)

    def _get(self, path, dtype: typing.Type[marshmallow.Schema], options):
        if not path.startswith("v2/"):
            raise CommandError("Invalid request path")

        fpath = "cache/" + path.replace("/", "_") + ".json"
        if not os.path.exists("cache"):
            os.mkdir("cache")

        key = settings.GW2_API_KEY

        obj = requests.get(
            f"https://api.guildwars2.com/{path}",
            headers={
                "Authorization": f"Bearer {key}",
                "X-Schema-Version": "latest",
            },
        ).json()

        with open(fpath, "wt") as o:
            json.dump(obj, o, indent=4)

        if dtype:
            multi = options["multi"]
            obj = dtype().load(obj, many=multi, unknown="EXCLUDE")
        self.print(obj)

    def _load(self, path, dtype: typing.Type[marshmallow.Schema], options):
        multi = options["multi"]
        with open(path, "rt") as f:
            data = json.load(f)

        obj = dtype().load(data, many=multi, unknown="EXCLUDE")
        if options["items"]:
            inventory = set(dto.CharacterSchema.get_item_id_list(obj))
            self.print("length: " + str(len(inventory)), inventory)
        else:
            self.print(obj)

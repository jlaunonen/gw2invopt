# -*- coding: utf-8 -*-
import typing

from django.db.transaction import atomic
from django.utils.timezone import now
from django.utils.translation import gettext

from .gw_client import Client
from .models import Character, Item, ItemSlot, PendingData


class Progress:
    def __init__(self, progress: typing.Callable[[], None]):
        self.target = 0
        self.current = 0
        self.errors = []
        self.progress = progress

    def add_target(self, n=1):
        self.target += n
        self.on_update()

    def add_current(self, n=1):
        self.current += n
        self.on_update()

    def add_error(self, e):
        self.errors.append(e)

    def on_update(self):
        self.progress()


def update_characters(progress: Progress):
    client = Client()

    existing_characters = set(Character.objects.values_list("name", flat=True))
    characters: typing.Set[str] = set(client.get_characters())

    new_characters = characters - existing_characters
    extra_characters = existing_characters - characters
    updates = existing_characters & characters

    if extra_characters:
        progress.add_target()
        (Character.objects.filter(name__in=extra_characters).update(deleted=True))
        progress.add_current()

    pending = []
    if new_characters:
        progress.add_target(len(new_characters))
        pending.extend(
            PendingData(
                target=PendingData.TargetChoices.CHARACTER, api_id=char, json=""
            )
            for char in new_characters
        )

    if updates:
        progress.add_target(len(updates))
        pending.extend(
            PendingData(
                target=PendingData.TargetChoices.CHARACTER,
                api_id=char,
                json="",
                is_update=True,
            )
            for char in updates
        )

    if pending:
        PendingData.objects.bulk_create(pending)

    for pending in PendingData.objects.filter(
        target=PendingData.TargetChoices.CHARACTER,
        completed__isnull=True,
        failed_count__lt=PendingData.FAILED_REPEAT_COUNT,
    ):
        _update_character(pending, progress, client)


def _update_character(pending: PendingData, progress: Progress, client: Client):
    is_update = pending.is_update
    char_id = pending.api_id
    try:
        data = client.get_character_core(char_id)
        with atomic():
            _, created = Character.objects.update_or_create(defaults=data, name=char_id)
            if is_update == created:
                # Inverse condition, as which is the unexpected one.
                print("Unexpected", "create" if is_update else "update", "for", char_id)
            pending.completed = now()
            pending.save()
    except Exception as e:
        progress.add_error(gettext("Failed to update character {}").format(char_id))
        print("Failed to update {}:".format(char_id), e)
        pending.failed = now()
        pending.failed_count += 1
        pending.save()

    progress.add_current()


def update_character_inventory(progress: Progress):
    client = Client()
    # TODO ...
    pass

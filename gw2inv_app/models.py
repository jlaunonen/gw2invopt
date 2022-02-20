# -*- coding: utf-8 -*-

import typing

from django.db import models
from django.utils.translation import gettext_lazy as _


class FlagCharField(models.CharField):
    """List of flags"""

    def __init__(self, choices, separator=",", *args, **kwargs):
        self.separator = separator
        super().__init__(*args, choices=choices, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if self.separator != ",":
            kwargs["separator"] = self.separator
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        v = self._stable_list(value)
        return self.separator.join(v)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.split(self.separator)
        return self._stable_list(value)

    @staticmethod
    def _stable_list(value: typing.List[str]) -> typing.List[str]:
        if not isinstance(value, list):
            value = list(value)
        value.sort()
        return value


class Race(models.TextChoices):
    ASURA = "Asura", _("Asura")
    CHARR = "Charr", _("Charr")
    HUMAN = "Human", _("Human")
    NORN = "Norn", _("Norn")
    SYLVARI = "Sylvari", _("Sylvari")


class Profession(models.TextChoices):
    ELEMENTALIST = "Elementalist", _("Elementalist")
    ENGINEER = "Engineer", _("Engineer")
    GUARDIAN = "Guardian", _("Guardian")
    MESMER = "Mesmer", _("Mesmer")
    NECROMANCER = "Necromancer", _("Necromancer")
    RANGER = "Ranger", _("Ranger")
    REVENANT = "Revenant", _("Revenant")
    THIEF = "Thief", _("Thief")
    WARRIOR = "Warrior", _("Warrior")


class Restriction(models.TextChoices):
    ASURA = "Asura", _("Asura")
    CHARR = "Charr", _("Charr")
    FEMALE = "Female", _("Female")
    HUMAN = "Human", _("Human")
    NORN = "Norn", _("Norn")
    SYLVARI = "Sylvari", _("Sylvari")
    ELEMENTALIST = "Elementalist", _("Elementalist")
    ENGINEER = "Engineer", _("Engineer")
    GUARDIAN = "Guardian", _("Guardian")
    MESMER = "Mesmer", _("Mesmer")
    NECROMANCER = "Necromancer", _("Necromancer")
    RANGER = "Ranger", _("Ranger")
    THIEF = "Thief", _("Thief")
    WARRIOR = "Warrior", _("Warrior")


class Character(models.Model):
    name = models.CharField(max_length=255, unique=True)
    race = models.CharField(max_length=32, choices=Race.choices)
    profession = models.CharField(max_length=32, choices=Profession.choices)
    level = models.PositiveIntegerField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, level {self.level} {self.race} {self.profession}"


class Item(models.Model):
    class Type(models.TextChoices):
        ARMOR = "Armor", _("Armor")
        BACK = "Back", _("Back")
        BAG = "Bag", _("Bag")
        CONSUMABLE = "Consumable", _("Consumable")
        CONTAINER = "Container", _("Container")
        CRAFTING_MATERIAL = "CraftingMaterial", _("Crafting material")
        GATHERING = "Gathering", _("Gathering tool")
        GIZMO = "Gizmo", _("Gizmo")
        KEY = "Key", _("Key")
        MINIATURE = "MiniPet", _("Miniature")
        TOOL = "Tool", _("Salvage kit")
        TRAIT = "Trait", _("Trait guide")
        TRINKET = "Trinket", _("Trinket")
        TROPHY = "Trophy", _("Trophy")
        UPGRADE_COMPONENT = "UpgradeComponent", _("Upgrade component")
        WEAPON = "Weapon", _("Weapon")

    class Rarity(models.TextChoices):
        JUNK = "Junk", _("Junk")
        BASIC = "Basic", _("Basic")
        FINE = "Fine", _("Fine")
        MASTERWORK = "Masterwork", _("Masterwork")
        RARE = "Rare", _("Rare")
        EXOTIC = "Exotic", _("Exotic")
        ASCENDED = "Ascended", _("Ascended")
        LEGENDARY = "Legendary", _("Legendary")

    class Flags(models.TextChoices):
        ACCOUNT_BIND_ON_USE = "AccountBindOnUse", _("Account bound on use")
        ACCOUNT_BOUND = "AccountBound", _("Account bound on acquire")
        ATTUNED = "Attuned", _("If the item is Attuned")
        BULK_CONSUME = "BulkConsume", _("If the item can be bulk consumed")
        DELETE_WARNING = "DeleteWarning", _(
            "If the item will prompt the player with a warning when deleting"
        )
        HIDE_SUFFIX = "HideSuffix", _("Hide the suffix of the upgrade component")
        INFUSED = "Infused", _("If the item is infused")
        MONSTER_ONLY = "MonsterOnly", _("(monster only)")
        NO_MYSTIC_FORGE = "NoMysticForge", _("Not usable in the Mystic Forge")
        NO_SALVAGE = "NoSalvage", _("Not salvageable")
        NO_SELL = "NoSell", _("Not sellable")
        NOT_UPGRADEABLE = "NotUpgradeable", _("Not upgradeable")
        NO_UNDERWATER = "NoUnderwater", _("Not available underwater")
        SOUL_BIND_ON_ACQUIRE = "SoulbindOnAcquire", _("Soulbound on acquire")
        SOUL_BIND_ON_USE = "SoulBindOnUse", _("Soulbound on use")
        TONIC = "Tonic", _("If the item is a tonic")
        UNIQUE = "Unique", _("Unique")

    name = models.CharField(max_length=255)
    chat_link = models.CharField(max_length=32)
    icon_url = models.URLField(null=True)
    description = models.TextField()
    type = models.CharField(max_length=64, choices=Type.choices)
    rarity = models.CharField(max_length=64, choices=Rarity.choices)
    flags = FlagCharField(
        max_length=255, choices=Flags.choices
    )  # Comma-separated list of Flags
    level = models.PositiveSmallIntegerField()
    restrictions = FlagCharField(
        max_length=255, choices=Restriction.choices
    )  # Comma-separated list of Restriction

    def __str__(self):
        return f"{self.name}, level {self.level} {self.rarity} {self.type}"


class ItemSlot(models.Model):
    class BindingChoices(models.TextChoices):
        ACCOUNT = "Account", _("Account bound")
        CHARACTER = "Character", _("Soulbound to {}")

    character = models.ForeignKey(
        Character, null=True, on_delete=models.CASCADE, related_name="slots"
    )
    item = models.ForeignKey(Item, on_delete=models.RESTRICT, related_name="in_slots")
    count = models.PositiveIntegerField(default=1)
    charges = models.PositiveIntegerField(null=True, blank=True)

    binding = models.CharField(
        max_length=32, choices=BindingChoices.choices, null=True, blank=True
    )
    bound_to = models.ForeignKey(
        Character, null=True, on_delete=models.DO_NOTHING, related_name="bound_slots"
    )  # db_constraint=False ?
    upgrades = models.ManyToManyField(Item, related_name="as_upgrades")
    infusions = models.ManyToManyField(Item, related_name="as_infusions")

    def get_binding(self) -> str:
        if self.binding is None:
            return ""

        to = self.bound_to
        if to is not None:
            return self.binding.label.format(to.name)
        return self.binding.label

    def __str__(self):
        return f"{self.count}x {self.item}"


class PendingData(models.Model):
    class TargetChoices(models.TextChoices):
        CHARACTER = "Character"
        ITEM = "Item"
        SLOT = "Slot"

    FAILED_REPEAT_COUNT = 3

    target = models.CharField(max_length=32, choices=TargetChoices.choices)
    api_id = models.CharField(max_length=64, verbose_name=_("API ID, int/str"))
    json = models.TextField()
    is_update = models.BooleanField(default=False)
    completed = models.DateTimeField(null=True)
    failed = models.DateTimeField(null=True)
    failed_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Pending {self.target} info, id {self.api_id}"

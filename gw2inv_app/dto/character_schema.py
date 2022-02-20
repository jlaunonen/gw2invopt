# -*- coding: utf-8 -*-
import typing

from marshmallow import Schema, fields, pre_load

from .item_slot import ItemSlotMixin


class InventorySchema(Schema, ItemSlotMixin):
    class Meta:
        unknown = "EXCLUDE"

    @pre_load(pass_many=True)
    def unwrap(self, data, **kwargs):
        # Remove null list elements.
        return [el for el in data if el is not None]


class BagsSchema(Schema):
    """
    bags (array) - Contains one object structure per bag in the character's inventory
    id (integer) - The bag's item id which can be resolved against /v2/items
    size (integer) - The amount of slots available with this bag.
    inventory (array) - Contains one object structure per item, object is null if no item is in the given bag slot.
        id (integer) - The item id which can be resolved against /v2/items
        count (integer) - Amount of item in the stack. Minium of 1, maximum of 250.
        infusions (array) (optional) - returns an array of infusion item ids which can be resolved against /v2/items
        upgrades (array) (optional) - returns an array of upgrade component item ids which can be resolved against /v2/items
        skin (integer) (optional) - Skin id for the given equipment piece. Can be resolved against /v2/skins
        stats (object) (optional) - Contains information on the stats chosen if the item offers an option for stats/prefix.
            id (integer) - The itemstat id, can be resolved against /v2/itemstats.
            attributes (object) - Contains a summary of the stats on the item.
                Power (integer) (optional) - Shows the amount of power given
                Precision (integer) (optional) - Shows the amount of Precision given
                Toughness (integer) (optional) - Shows the amount of Toughness given
                Vitality (integer) (optional) - Shows the amount of Vitality given
                Condition Damage (integer) (optional) - Shows the amount of Condition Damage given
                Condition Duration (integer) (optional) - Shows the amount of Condition Duration given
                Healing (integer) (optional) - Shows the amount of Healing Power given
                BoonDuration (integer) (optional) - Shows the amount of Boon Duration given
        binding (string) (optional) - describes which kind of binding the item has. Possible values:
            Character
            Account
        bound_to (string) (optional, only if character bound) - Name of the character the item is bound to.
    """

    class Meta:
        unknown = "EXCLUDE"

    inventory = fields.Nested(InventorySchema, many=True)


class EquipmentSchema(Schema):
    """
    equipment (array) - An array containing an entry for each piece of equipment currently on the selected character.
    id (integer) - The item id, resolvable against /v2/items
    slot (string) - The equipment slot in which the item is slotted. Possible values:
        HelmAquatic
        Backpack
        Coat
        Boots
        Gloves
        Helm
        Leggings
        Shoulders
        Accessory1
        Accessory2
        Ring1
        Ring2
        Amulet
        WeaponAquaticA
        WeaponAquaticB
        WeaponA1
        WeaponA2
        WeaponB1
        WeaponB2
        Sickle
        Axe
        Pick
    infusions (array) (optional) - returns an array of infusion item ids which can be resolved against /v2/items
    upgrades (array) (optional) - returns an array of upgrade component item ids which can be resolved against /v2/items
    skin (integer) (optional) - Skin id for the given equipment piece. Can be resolved against /v2/skins
    stats (object) (optional) - Contains information on the stats chosen if the item offers an option for stats/prefix.
        id (integer) - The itemstat id, can be resolved against /v2/itemstats.
        attributes (object) - Contains a summary of the stats on the item.
            Power (integer) (optional) - Shows the amount of power given
            Precision (integer) (optional) - Shows the amount of Precision given
            Toughness (integer) (optional) - Shows the amount of Toughness given
            Vitality (integer) (optional) - Shows the amount of Vitality given
            Condition Damage (integer) (optional) - Shows the amount of Condition Damage given
            Condition Duration (integer) (optional) - Shows the amount of Condition Duration given
            Healing (integer) (optional) - Shows the amount of Healing Power given
            BoonDuration (integer) (optional) - Shows the amount of Boon Duration given
    binding (string) (optional) - describes which kind of binding the item has. Possible values:
        Character
        Account
    charges (number) (optional) - The amount of charges remaining on the item.
    bound_to (string) (optional, only if character bound) - Name of the character the item is bound to.
    dyes (array of numbers) - Array of selected dyes for the equipment piece. Values default to null if no dye is selected. Colors can be resolved against v2/colors
    """

    class Meta:
        unknown = "EXCLUDE"

    id = fields.Integer(required=True)
    slot = fields.String()
    binding = fields.String()
    upgrades = fields.List(fields.Integer())


class CoreSchemaMixin:
    name = fields.String(required=True)
    race = fields.String(required=True)
    profession = fields.String(required=True)
    level = fields.Integer(required=True)


class CoreSchema(Schema, CoreSchemaMixin):
    """
    name (string) - The character's name.
    race (string) - The character's race. Possible values:
        Asura
        Charr
        Human
        Norn
        Sylvari
    gender (string) - The character's gender. Possible values:
        Male
        Female
    profession (string) - The character's profession. Possible values:
        Elementalist
        Engineer
        Guardian
        Mesmer
        Necromancer
        Ranger
        Revenant
        Thief
        Warrior
    level (integer) - The character's level.
    guild (string, optional) - The guild ID of the character's currently represented guild.
    age (integer) - The amount of seconds this character was played.
    created (string) - ISO 8601 representation of the character's creation time.
    deaths (integer) - The amount of times this character has been defeated.
    title (number, optional) - The currently selected title for the character. References /v2/titles.
    """

    pass


class CharacterSchema(Schema, CoreSchemaMixin):
    """
    AVOID USING (retrieves too much data).

    v2/characters/:id/backstory
    v2/characters/:id/core
    v2/characters/:id/crafting
    v2/characters/:id/equipment
    v2/characters/:id/heropoints
    v2/characters/:id/inventory
    v2/characters/:id/recipes
    v2/characters/:id/sab
    v2/characters/:id/skills
    v2/characters/:id/specializations
    v2/characters/:id/training
    """

    class Meta:
        unknown = "EXCLUDE"

    bags = fields.Nested(BagsSchema, many=True)
    equipment = fields.Nested(EquipmentSchema, many=True)

    @staticmethod
    def get_item_id_list(character: typing.Dict):
        for bag in character["bags"]:
            yield from (i["id"] for i in bag["inventory"])


class EquipmentResponseSchema(Schema):
    """v2/characters/:id/equipment"""

    equipment = fields.Nested(EquipmentSchema, many=True)


class InventoryResponseSchema(Schema):
    """v2/characters/:id/inventory"""

    bags = fields.Nested(BagsSchema, many=True)

# -*- coding: utf-8 -*-

from marshmallow import fields


class ItemSlotMixin:
    """
    Item slot properties for BankSchema and CharacterSchema.bags.inventory.

    id (number) – The item's ID.
    count (number) – The amount of items in the item stack.
    charges (number, optional) – The amount of charges remaining on the item.
    skin (number, optional) – The skin applied to the item, if it is different from its original. Can be resolved against /v2/skins.
    dyes (array of numbers, optional) – The IDs of the dyes applied to the item. Can be resolved against /v2/colors.
    upgrades (array of numbers, optional) – The item IDs of the runes or sigils applied to the item.
    upgrade_slot_indices (array of numbers, optional) – The slot occupied by the upgrade at the corresponding position in upgrades.
    infusions (array, optional) – An array of item IDs for each infusion applied to the item.
    binding (string, optional) – The current binding of the item. Either Account or Character if present.
    bound_to (string, optional) – If binding is Character, this field tells which character it is bound to.
    stats (object, optional) – The stats of the item.
        id – The ID of the item's stats. Can be resolved against /v2/itemstats.
        attributes (array of key/value pairs) (default/null value: {} empty array) - The list of stats provided by this item. May include the following:
            AgonyResistance (decimal) - Agony Resistance
            BoonDuration (decimal) - Concentration
            ConditionDamage (decimal) – Condition Damage
            ConditionDuration (decimal) - Expertise
            CritDamage (decimal) – Ferocity
            Healing (decimal) – Healing Power
            Power (decimal) – Power
            Precision (decimal) – Precision
            Toughness (decimal) – Toughness
            Vitality (decimal) – Vitality
    """

    id = fields.Integer(required=True)
    count = fields.Integer()
    binding = fields.String()
    bound_to = fields.String()
    upgrades = fields.List(fields.Integer())
    upgrade_slot_indices = fields.List(fields.Integer())

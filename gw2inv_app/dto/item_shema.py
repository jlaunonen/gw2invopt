# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, validate

from gw2inv_app.models import Item as ModelItem
from gw2inv_app.models import Race


class ItemSchema(Schema):
    """
    v2/items/{id} -> ItemSchema

    id (number) – The item id.
    chat_link (string) – The chat link.
    name (string) – The item name.
    icon (string, optional) – The full icon URL.
    description (string, optional) – The item description.
    type (string) – The item type (see below). Possible values:
        Armor – Armor
        Back – Back item
        Bag – Bags
        Consumable – Consumables
        Container – Containers
        CraftingMaterial – Crafting materials
        Gathering – Gathering tools
        Gizmo – Gizmos
        Key
        MiniPet – Miniatures
        Tool – Salvage kits
        Trait – Trait guides
        Trinket – Trinkets
        Trophy – Trophies
        UpgradeComponent – Upgrade components
        Weapon – Weapons
    rarity (string) – The item rarity. Possible values:
        Junk
        Basic
        Fine
        Masterwork
        Rare
        Exotic
        Ascended
        Legendary
    level (number) – The required level.
    vendor_value (number) – The value in coins when selling to a vendor. (Can be non-zero even when the item has the NoSell flag.)
    default_skin (number, optional) – The default skin id.
    flags (array of strings) – Flags applying to the item. Possible values:
        AccountBindOnUse – Account bound on use
        AccountBound – Account bound on acquire
        Attuned - If the item is Attuned
        BulkConsume - If the item can be bulk consumed
        DeleteWarning - If the item will prompt the player with a warning when deleting
        HideSuffix – Hide the suffix of the upgrade component
        Infused - If the item is infused
        MonsterOnly
        NoMysticForge – Not usable in the Mystic Forge
        NoSalvage – Not salvageable
        NoSell – Not sellable
        NotUpgradeable – Not upgradeable
        NoUnderwater – Not available underwater
        SoulbindOnAcquire – Soulbound on acquire
        SoulBindOnUse – Soulbound on use
        Tonic - If the item is a tonic
        Unique – Unique
    game_types (array of strings) – The game types in which the item is usable. At least one game type is specified. Possible values:
        Activity – Usable in activities
        Dungeon – Usable in dungeons
        Pve – Usable in general PvE
        Pvp – Usable in PvP
        PvpLobby – Usable in the Heart of the Mists
        Wvw – Usable in World vs. World
    restrictions (array of strings) – Restrictions applied to the item. Possible values:
        Asura
        Charr
        Female
        Human
        Norn
        Sylvari
        Elementalist
        Engineer
        Guardian
        Mesmer
        Necromancer
        Ranger
        Thief
        Warrior
    upgrades_into (array, optional) – Lists what items this item can be upgraded into, and the method of upgrading. Each object in the array has the following attributes:
        upgrade (string) – Describes the method of upgrading. Possible values:
            Attunement
            Infusion
        item_id (integer) – The item ID that results from performing the upgrade.
    upgrades_from (array, optional) – Lists what items this item can be upgraded from, and the method of upgrading. See upgrades_into for format.
    details (object, optional) – Additional item details if applicable, depending on the item type (see below).
    """

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    chat_link = fields.String(required=True)
    icon_url = fields.Url()
    description = fields.String()
    type = fields.String(required=True, validate=validate.OneOf(ModelItem.Type.values))
    rarity = fields.String(
        required=True, validate=validate.OneOf(ModelItem.Rarity.values)
    )
    flags = fields.List(
        fields.String(validate=validate.OneOf(ModelItem.Flags.values)), required=True
    )
    level = fields.Integer(required=True)
    restrictions = fields.List(fields.String(validate=validate.OneOf(Race.values)))

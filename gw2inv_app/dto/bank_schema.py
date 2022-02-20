# -*- coding: utf-8 -*-

from marshmallow import Schema, pre_load

from .item_slot import ItemSlotMixin


class BankSchema(Schema, ItemSlotMixin):
    """
    v2/account/bank -> List[Optional[BankSchema]]

    """

    @pre_load(pass_many=True)
    def unwrap(self, data, **kwargs):
        # Remove null list elements.
        return [el for el in data if el is not None]

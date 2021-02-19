# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from acmesky.models.base_model_ import Model
from acmesky import util


class PaymentInformation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, transaction_id=None, status=None):  # noqa: E501
        """PaymentInformation - a model defined in OpenAPI

        :param transaction_id: The transaction_id of this PaymentInformation.  # noqa: E501
        :type transaction_id: str
        :param status: The status of this PaymentInformation.  # noqa: E501
        :type status: bool
        """
        self.openapi_types = {
            'transaction_id': str,
            'status': bool
        }

        self.attribute_map = {
            'transaction_id': 'transaction_id',
            'status': 'status'
        }

        self._transaction_id = transaction_id
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'PaymentInformation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PaymentInformation of this PaymentInformation.  # noqa: E501
        :rtype: PaymentInformation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def transaction_id(self):
        """Gets the transaction_id of this PaymentInformation.


        :return: The transaction_id of this PaymentInformation.
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this PaymentInformation.


        :param transaction_id: The transaction_id of this PaymentInformation.
        :type transaction_id: str
        """
        if transaction_id is None:
            raise ValueError("Invalid value for `transaction_id`, must not be `None`")  # noqa: E501

        self._transaction_id = transaction_id

    @property
    def status(self):
        """Gets the status of this PaymentInformation.


        :return: The status of this PaymentInformation.
        :rtype: bool
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PaymentInformation.


        :param status: The status of this PaymentInformation.
        :type status: bool
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

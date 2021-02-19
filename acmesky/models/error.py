# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from acmesky.models.base_model_ import Model
from acmesky import util


class Error(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, description=None):  # noqa: E501
        """Error - a model defined in OpenAPI

        :param description: The description of this Error.  # noqa: E501
        :type description: str
        """
        self.openapi_types = {
            'description': str
        }

        self.attribute_map = {
            'description': 'description'
        }

        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'Error':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Error of this Error.  # noqa: E501
        :rtype: Error
        """
        return util.deserialize_model(dikt, cls)

    @property
    def description(self):
        """Gets the description of this Error.


        :return: The description of this Error.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Error.


        :param description: The description of this Error.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if description is not None and len(description) < 1:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

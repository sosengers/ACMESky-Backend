# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from acmesky.models.error import Error  # noqa: E501
from acmesky.models.flight import Flight  # noqa: E501
from acmesky.models.interest import Interest  # noqa: E501
from acmesky.models.offer_purchase_data import OfferPurchaseData  # noqa: E501
from acmesky.models.payment_information import PaymentInformation  # noqa: E501
from acmesky.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    @unittest.skip("Connexion does not support multiple consummes. See https://github.com/zalando/connexion/pull/760")
    def test_buy_offer(self):
        """Test case for buy_offer

        buyOffer
        """
        offer_purchase_data = {
  "address" : {
    "number" : "number",
    "country" : "country",
    "city" : "city",
    "street" : "street",
    "zip_code" : "zip_code"
  },
  "surname" : "surname",
  "name" : "name",
  "offer_code" : "offer_code"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/offers/buy',
            method='POST',
            headers=headers,
            data=json.dumps(offer_purchase_data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_publish_last_minute_offer(self):
        """Test case for publish_last_minute_offer

        publishLastMinuteOffer
        """
        flight = {
  "arrival_datetime" : "2000-01-23T04:56:07.000+00:00",
  "cost" : 0.08008281904610115,
  "departure_airport_code" : "departure_airport_code",
  "arrival_airport_code" : "arrival_airport_code",
  "flight_id" : "flight_id",
  "departure_datetime" : "2000-01-23T04:56:07.000+00:00"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/offers/lastminute',
            method='POST',
            headers=headers,
            data=json.dumps(flight),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_interest(self):
        """Test case for register_interest

        registerInterest
        """
        interest = {
  "max_price" : 0.08008281904610115,
  "min_departure_date" : "2000-01-23",
  "prontogram_username" : "prontogram_username",
  "departure_airport_code" : "departure_airport_code",
  "arrival_airport_code" : "arrival_airport_code",
  "max_comeback_date" : "2000-01-23"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/interests',
            method='POST',
            headers=headers,
            data=json.dumps(interest),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_payment_information(self):
        """Test case for send_payment_information

        sendPaymentInformation
        """
        payment_information = {
  "transaction_id" : "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
  "status" : true
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/payments',
            method='POST',
            headers=headers,
            data=json.dumps(payment_information),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

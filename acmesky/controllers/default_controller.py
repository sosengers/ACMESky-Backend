from acmesky.models.buy_offer_response import BuyOfferResponse
import connexion
import six

from acmesky.models.error import Error  # noqa: E501
from acmesky.models.flight import Flight  # noqa: E501
from acmesky.models.interest import Interest  # noqa: E501
from acmesky.models.offer_purchase_data import OfferPurchaseData  # noqa: E501
from acmesky.models.payment_information import PaymentInformation  # noqa: E501
from acmesky import util

import json
from redis import Redis
import requests
import logging

from acmesky.camunda_connector.camunda_rest_client import send_string_as_correlate_message

camunda_base_url = "http://camunda_acmesky:8080/engine-rest"


def buy_offer(offer_purchase_data=None):  # noqa: E501
    """buyOffer

    Requires to start the buying process of the offer with the given offer code. API for: User # noqa: E501

    :param offer_purchase_data: 
    :type offer_purchase_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        offer_purchase_data = OfferPurchaseData.from_dict(connexion.request.get_json())  # noqa: E501
    pay_offer_url=str(hash((
            offer_purchase_data.offer_code,
            offer_purchase_data.name,
            offer_purchase_data.surname,
            hash((
                offer_purchase_data.address.street,
                offer_purchase_data.address.number,
                offer_purchase_data.address.city,
                offer_purchase_data.address.zip_code,
                offer_purchase_data.address.country))
        )
        ))

    r = send_string_as_correlate_message("offer_purchase_data", [("offer_purchase_data", json.dumps(offer_purchase_data.to_dict()))])
        #logging.error(f"DATA: {offer_purchase_data.to_dict()}")
    return BuyOfferResponse(pay_offer_url=pay_offer_url)


def publish_last_minute_offer(flights=None):  # noqa: E501
    """publishLastMinuteOffer

    Allows flight companies to notify ACMESky of the presence of new last minute offers. API for: Flight Company # noqa: E501

    :param flights:
    :type flights: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        flights = [Flight.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

    for flight in flights:
        flight.departure_datetime = flight.departure_datetime.isoformat()
        flight.arrival_datetime = flight.arrival_datetime.isoformat()

    flights_dict = [f.to_dict() for f in flights]

    r = send_string_as_correlate_message("offers", [("offers", json.dumps(flights_dict))])
    return None, r.status_code


def register_interest(interest=None):  # noqa: E501
    """registerInterest

    Register the user interest for roundtrip flights. API for: User # noqa: E501

    :param interest: 
    :type interest: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        interest = Interest.from_dict(connexion.request.get_json())  # noqa: E501

    interest_dict = interest.to_dict()
    interest_dict['min_departure_date'] = interest.min_departure_date.isoformat()
    interest_dict['max_comeback_date'] = interest.max_comeback_date.isoformat()

    # Send message to Camunda
    r = send_string_as_correlate_message("interest", [("interest", json.dumps(interest_dict))])
    if r.status_code >= 300:
        logging.error(f"Fail to send message to Camunda. Response: {r.text}")
    return None, r.status_code


def send_payment_information(payment_information=None):  # noqa: E501
    """sendPaymentInformation

    Sends the information received by the user for verification purposes. API for: Payment Provider # noqa: E501

    :param payment_information: 
    :type payment_information: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payment_information = PaymentInformation.from_dict(connexion.request.get_json())  # noqa: E501

    redis_connection = Redis(host="acmesky_redis", port=6379, db=0)
    process_instance_id = redis_connection.get(payment_information.transaction_id).decode("utf-8")
    redis_connection.close()

    r = send_string_as_correlate_message("payment_status", [("payment_status", json.dumps(payment_information.to_dict()))], process_instance_id)
    if r.status_code >= 300:
        logging.error(f"Fail to send message to Camunda. Response: {r.text}")
    return None, r.status_code

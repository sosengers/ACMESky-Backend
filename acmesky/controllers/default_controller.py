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

    """ Communication code generation
        The communication code will be used to communicate with the WebSocket. It is some unique data hashed altogether.
    """
    communication_code = str(hash((
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

    """ Sending as a correlate message to Camunda the data inserted by the user
    """
    r = send_string_as_correlate_message("offer_purchase_data",
                                         [("offer_purchase_data", json.dumps(offer_purchase_data.to_dict()))])

    """ Returning to the user the communication code to use with the WebSocket
    """
    return BuyOfferResponse(communication_code=communication_code)


def publish_last_minute_offer(company_name, flight=None):  # noqa: E501
    """publishLastMinuteOffer

    Allows flight companies to notify ACMESky of the presence of new last minute offers. API for: Flight Company # noqa: E501

    :param company_name: Name of the flight company
    :type company_name: str
    :param flight:
    :type flight: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        flights = [Flight.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

    """ Convert the datetime to iso format
        For each flights sent, the datetimes is converted in theit iso format 
    """
    for flight in flights:
        flight.departure_datetime = flight.departure_datetime.isoformat()
        flight.arrival_datetime = flight.arrival_datetime.isoformat()

    """ Generate the list of flights in their dict format to send to Camunda within a correlate message
    """
    flights_dict = [f.to_dict() for f in flights]
    r = send_string_as_correlate_message("offers",
                                         [("offers", json.dumps(flights_dict)), ("company_name", str(company_name))])
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

    """ Convert the datetimes into their iso format
    """
    interest_dict = interest.to_dict()
    interest_dict['min_departure_date'] = interest.min_departure_date.isoformat()
    interest_dict['max_comeback_date'] = interest.max_comeback_date.isoformat()

    """ Send message with the interest to Camunda
    """
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

    """ Open the connection to redis to get the right process instance id in the Camunda Engine (saved by a worker)
    """
    redis_connection = Redis(host="acmesky_redis", port=6379, db=0)
    process_instance_id = redis_connection.get(payment_information.transaction_id).decode("utf-8")
    redis_connection.close()

    """ Send a correlate message to Camunda with the information about the payment status. The message is for a specific
        process instance, identified by the process_instance_id variable 
    """
    r = send_string_as_correlate_message("payment_status",
                                         [("payment_status", json.dumps(payment_information.to_dict()))],
                                         process_instance_id)
    if r.status_code >= 300:
        logging.error(f"Fail to send message to Camunda. Response: {r.text}")
    return None, r.status_code

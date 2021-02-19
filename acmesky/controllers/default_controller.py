import connexion
import six

from acmesky.models.error import Error  # noqa: E501
from acmesky.models.flight import Flight  # noqa: E501
from acmesky.models.interest import Interest  # noqa: E501
from acmesky.models.offer_purchase_data import OfferPurchaseData  # noqa: E501
from acmesky.models.payment_information import PaymentInformation  # noqa: E501
from acmesky import util

from pymongo import MongoClient

def buy_offer(offer_purchase_data=None):  # noqa: E501
    """buyOffer

    Requires to start the buying process of the offer with the given offer code. API for: User # noqa: E501

    :param offer_purchase_data: 
    :type offer_purchase_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        offer_purchase_data = OfferPurchaseData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def publish_last_minute_offer(flight=None):  # noqa: E501
    """publishLastMinuteOffer

    Allows flight companies to notify ACMESky of the presence of new last minute offers. API for: Flight Company # noqa: E501

    :param flight: 
    :type flight: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        flight = [Flight.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def register_interest(interest=None):  # noqa: E501
    """registerInterest

    Register the user interest for roundtrip flights. API for: User # noqa: E501

    :param interest: 
    :type interest: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        interest = Interest.from_dict(connexion.request.get_json())  # noqa: E501

    username = "root"
    password = "password"
    client = MongoClient(f"mongodb://{username}:{password}@acmesky_mongo:27017")
    acmesky_db = client['ACMESky']
    interests_collection = acmesky_db['interests']
    interest_dict = interest.to_dict()
    interest_dict['min_departure_date'] = interest.min_departure_date.isoformat()
    interest_dict['max_comeback_date'] = interest.max_comeback_date.isoformat()
    if interests_collection.find_one(interest_dict):
        return (None, 200)
    else:
        interests_collection.insert_one(interest_dict)
        return (None, 200)


def send_payment_information(payment_information=None):  # noqa: E501
    """sendPaymentInformation

    Sends the information received by the user for verification purposes. API for: Payment Provider # noqa: E501

    :param payment_information: 
    :type payment_information: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payment_information = PaymentInformation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

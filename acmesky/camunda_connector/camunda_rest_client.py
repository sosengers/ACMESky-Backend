import requests
from os import environ
import logging

BASE_URL: str = environ.get("CAMUNDA_BASE_URL", "http://camunda_acmesky:8080/engine-rest")


def send_string_as_correlate_message(name: str, process_variables: list[tuple[str, str]], process_instance_id=None):
    """
    Send to Camunda Engine a correlate message with some process variables and an optional process_instance_id
    @param name: the name of the message, used by the engine to know which Message Catch Event trigger
    @param process_variables: the variables to pass to the process with the message
    @param process_instance_id: the process instance id to use to correlate a message to a started process instance
    @return: return the status code returned by Camunda
    """

    """ Generate a dictionary with the variables to send to Camunda 
    """
    process_variables_dict = {}
    for variable in process_variables:
        variable_name = variable[0]
        variable_value = variable[1]

        process_variables_dict[variable_name] = {
            "value": variable_value,
            "type": "String"
        }

    process_variables_dict["valueInfo"] = {
        "transient": True
    }

    """ Create the message to send to Camunda starting from the parameters
    """
    camunda_message = {
        "messageName": name,
        "processInstanceId": process_instance_id,
        "processVariables": process_variables_dict
    } if process_instance_id else {
        "messageName": name,
        "processVariables": process_variables_dict
    }
    logging.info(camunda_message)
    return requests.post(BASE_URL + "/message", json=camunda_message)

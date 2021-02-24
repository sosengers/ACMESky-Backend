import requests
from os import environ

BASE_URL: str = environ.get("CAMUNDA_BASE_URL", "http://camunda_acmesky:8080/engine-rest")

def send_string_as_correlate_message(name: str, process_variables: list[tuple[str, str]]):
    process_variables_dict = {}
    for variable in process_variables:
        variable_name = variable[0]
        variable_value = variable[1]

        process_variables_dict[variable_name] = {
            "value": variable_value,
            "type": "String",
            "valueInfo": {
                "transient": True
            }
        }

    camunda_message = {
        "messageName": name,
        "processVariables": process_variables_dict
    }

    return requests.post(BASE_URL+"/message", json=camunda_message)


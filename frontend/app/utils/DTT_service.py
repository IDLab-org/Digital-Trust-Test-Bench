from flask import session
import json, requests
from config import Config


class DTT_service:
    """
    Encapsulates all calls to the DTT service
    """

    def request(method, route, json_params="", api_token=""):
        """
        Sends a  request to the DTT service
        Input:
                method: 'get', 'post', 'delete', ...
                route : The route to call (include leading slash):
                    Example: /login, or /users/12345
                json_params: a json object for requests that require
                api_token: the user's DTT-Service authentication token

        Returns:
             requests.Response object.
        """
        apiurl = f"{Config.DTT_SERVICE_URL}{route}"

        # print(f'Method={method}, URL={apiurl}, jsonparams={json_params}, token={api_token}')

        try:
            match method:
                case "get":
                    response = requests.get(url=apiurl, headers=api_token)

                case "post":
                    response = requests.post(
                        url=apiurl, json=json_params, headers=api_token
                    )

                case "put":
                    response = requests.put(
                        url=apiurl, json=json_params, headers=api_token
                    )

                case "delete":
                    response = requests.delete(
                        url=apiurl, json=json_params, headers=api_token
                    )
                case _:
                    response = {}  ## TBD: figure a better default value

        except:
            print("Service unavailable")
            response = (
                requests.Response()
            )  ## TBD: Properly set a response object to indicate that the DTT service is not available

        return response

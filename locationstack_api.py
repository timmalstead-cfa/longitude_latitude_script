from http import client
from urllib import parse
from json import loads

try:
    with open("./location_api_key.txt") as key_data:
        forward_geolocation_string: str = "api.positionstack.com"

        params = parse.urlencode({
            "access_key": key_data.read(),
            "query": "1107 San Andres Street, Santa Barbara, CA 93101",
            "limit": 1,
        })

        request_string: str = '/v1/forward?{}'.format(params)

        print(request_string)

        api_interface: client.HTTPConnection = client.HTTPConnection(
            forward_geolocation_string)
        api_interface.request("GET", request_string)

        response: client.HTTPResponse = api_interface.getresponse()
        data: bytes = response.read()

        returned_location_json: str = data.decode()

        translated_dict = loads(returned_location_json)

        print(translated_dict["data"][0])
except Exception as error:
    print(f"#{error.__class__} occured when trying to contact the API.")

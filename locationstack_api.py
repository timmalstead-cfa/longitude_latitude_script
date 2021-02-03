from typing import List, Dict
from http import client
from urllib import parse
from json import loads
from asyncio import sleep, run

fetched_data: List[Dict] = []


async def get_lat_long_data():
    try:
        total_calls: int = 0
        with open("./location_api_key.txt") as key_data:
            access_key: str = key_data.read()
            saved_json_data: List[Dict] = loads(
                open("./locations.json").read())
            converted_data: List[str] = list(map(
                lambda location: f"{location['address']}, {location['city']} {location['zip']}".strip(), saved_json_data))

            forward_geolocation_string: str = "api.positionstack.com"
            api_interface: client.HTTPConnection = client.HTTPConnection(
                forward_geolocation_string)

            for index, string in enumerate(converted_data):
                params = parse.urlencode({
                    "access_key": access_key,
                    "query": string,
                    "country": "US",
                    "region": "California",
                    "limit": 1,
                    "fields": "results.latitude,results.longitude"
                })

                request_string: str = '/v1/forward?{}'.format(params)

                attempts: int = 0
                continue_calling: bool = True

                while(continue_calling):
                    await sleep(.5)
                    api_interface.request("GET", request_string)
                    response: client.HTTPResponse = api_interface.getresponse()

                    data: bytes = response.read()

                    returned_location_json: str = data.decode()

                    translated_dict = loads(returned_location_json)
                    returned: str = str(translated_dict).strip()

                    total_calls += 1
                    print(attempts)
                    if(attempts >= 3):
                        failure: Dict = {
                            'failed_attempt': string, 'index': index}
                        fetched_data.append(failure)
                        continue_calling = False
                    elif(returned == "{'data': []}" or returned == "{'data': [[]]}"):
                        attempts += 1
                        continue
                    else:
                        fetched_data.append(translated_dict)
                        continue_calling = False

            print(total_calls)

    except Exception as error:
        print(f"#{error.__class__} occured when trying to contact the API.")

run(get_lat_long_data())

for data in fetched_data:
    print(data)

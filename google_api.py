from typing import List, Dict
from http import client
from urllib import parse
from json import dump, loads
from asyncio import sleep, run


async def get_lat_long_data():
    try:
        total_calls: int = 0
        current_list: List[Dict] = loads(
            open("./google_lat_long_info.json").read())

        # print(len(current_list))

        with open("./google_geocoding_api_key.txt") as key_data:
            key: str = key_data.read()

            saved_json_data: List[Dict] = loads(
                open("./locations_2.json").read())

            converted_data: List[str] = list(map(
                lambda location: f"{location['address']}, {location['city']} {location['zip']} CA USA".strip(), saved_json_data))

            forward_geolocation_string: str = "maps.googleapis.com"
            api_interface: client.HTTPSConnection = client.HTTPSConnection(
                forward_geolocation_string)

            for index, string in enumerate(converted_data):
                params = parse.urlencode({
                    "address": string,
                    "key": key
                })

                request_string: str = '/maps/api/geocode/json?{}'.format(
                    params)

                attempts: int = 0
                continue_calling: bool = True

                while(continue_calling):
                    await sleep(.05)
                    api_interface.request("GET", request_string)
                    response: client.HTTPResponse = api_interface.getresponse()

                    data: bytes = response.read()

                    returned_location_json: str = data.decode()

                    translated_dict = loads(returned_location_json)
                    returned: str = str(translated_dict).strip()

                    total_calls += 1
                    print(f"Attempts: {attempts}")
                    if(attempts >= 3):
                        failure: Dict = {
                            'failed_attempt': string, 'index': index}
                        current_list.append(failure)
                        continue_calling = False
                    elif(returned == "{'data': []}" or returned == "{'data': [[]]}"):
                        attempts += 1
                        continue
                    else:
                        current_list.append(translated_dict)
                        continue_calling = False
            with open('./google_lat_long_info_2.json', 'w') as json_to_save:
                dump(current_list, json_to_save)
            print(f"Total Calls: {total_calls}")

    except Exception as error:
        print(f"#{error.__class__} occured when trying to contact the API.")

run(get_lat_long_data())

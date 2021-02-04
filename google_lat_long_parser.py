from typing import List, Dict
from json import dump, loads


def parse_record(record: Dict) -> Dict:
    if(record["status"] == "REQUEST_DENIED"):
        del record["results"]
        return record
    else:
        return {"address": record["results"][0]["formatted_address"], "latitude": record["results"][0]["geometry"]["location"]["lat"], "longitude": record["results"][0]["geometry"]["location"]["lng"], "status": record["status"]}


google_list: List[Dict] = loads(
    open("./google_lat_long_info.json").read())

converted_list: List[Dict] = list(map(parse_record, google_list))

with open('./final_lat_long.json', 'w') as json_to_save:
    dump(converted_list, json_to_save)

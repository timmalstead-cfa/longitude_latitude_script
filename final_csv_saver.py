from typing import List, Dict
from json import loads

lat_string: str = ""
long_string: str = ""

final_list: List[Dict] = loads(
    open("./final_lat_long_2.json").read())

for record in final_list:
    lat_string += f"{record['latitude']}\n"
    long_string += f"{record['longitude']}\n"

with open('./latitude.csv', 'w') as lat_to_save:
    lat_to_save.write(lat_string)

with open('./longitude.csv', 'w') as long_to_save:
    long_to_save.write(long_string)

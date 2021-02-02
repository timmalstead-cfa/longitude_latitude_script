from typing import List, Dict
from json import dump
from csv import reader

list_of_locations: List[Dict] = []

try:
    with open("./locations.csv") as csv_data:
        csv_file: List = list(reader(csv_data, delimiter=","))

        city: str = csv_file[0][0].replace("\ufeff", "")
        address: str = csv_file[0][1]
        zip: str = csv_file[0][2]
        state: str = csv_file[0][3]
        id: str = csv_file[0][4]
        org_id: str = csv_file[0][5]

        for index, page in enumerate(csv_file):
            if(index == 0):
                continue
            else:
                location_info: Dict = {
                    city: page[0],
                    address: page[1],
                    zip: page[2],
                    state: page[3],
                    id: page[4],
                    org_id: page[5],
                }
                list_of_locations.append(location_info)
except Exception as error:
    print(f"#{error.__class__} occured when trying to parse the csv.")

with open('locations.json', 'w') as json_to_save:
    dump(list_of_locations, json_to_save)

# print(len(list_of_locations))

# for location in list_of_locations:
#     print(location)

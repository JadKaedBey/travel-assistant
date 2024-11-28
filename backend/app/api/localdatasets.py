"""
Author: Yogesh Kumar Srinivasan
Date: 24 November 2024
Usage:
    - Implementation of extracting the local data available against the GPE provided
"""
import csv
from typing import List

DATA_PATH = 'app/data/'
#To limit the output max to 10
OUTPUT_MAX = 10

def get_data(file_name: str, key: str, value: str, result_key: str) -> List[str]:
 
    file_path = f"{DATA_PATH}{file_name}.csv"
    data_list = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if key in row and row[key].lower() == value.lower():
                data_list.append(row[result_key])
                if len(data_list) >= OUTPUT_MAX:
                    break
    return data_list

def get_unesco_sites(gpe: str) -> List[str]:
    return get_data('unesco_sites', 'Country', gpe, 'Site Name')

def get_historical_places(gpe: str) -> List[str]:
    return get_data('US_Historic_Places', 'County', gpe, 'Resource_Name')

def get_hotels_motels(gpe: str) -> List[str]:
    return get_data('Hotels_Motels_LA', 'City', gpe, 'Business_Name')
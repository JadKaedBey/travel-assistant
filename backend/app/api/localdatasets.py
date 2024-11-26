import logging
import csv
from typing import List

DATA_PATH='app/data/'
output_max=10
def get_unesco_sites(gpe: str):
    with open(DATA_PATH+'unesco_sites.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';')
        data_list:list = []
        for row in reader:
            if 'Country' in row:
                if row['Country'].lower() == gpe.lower() :
                    data_list.append(row['Site Name'])
                if len(data_list) >= output_max:
                        break
    return data_list


def get_historical_places(gpe:str):
     with open(DATA_PATH+'US_Historic_Places.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';')
        data_list:list = []
        for row in reader:
            if 'County' in row:
                if row['County'].lower() == gpe.lower() :
                    data_list.append(row['Resource_Name'])
                if len(data_list) >= output_max:
                        break
        return data_list
     
def get_hotels_motels(gpe:str):
     with open(DATA_PATH+'Hotels_Motels_LA.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';')
        data_list:list = []
        for row in reader:
            if 'City' in row:
                if row['City'].lower() == gpe.lower() :
                    data_list.append(row['Business_Name']+row['Business_Type'])
                if len(data_list) >= output_max:
                        break
        return data_list
     
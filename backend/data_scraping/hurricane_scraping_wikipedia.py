from bs4 import BeautifulSoup
import csv
import requests
#hurricane_scraping.py has to be ran first
from hurricane_scraping import storms_with_quadrant_winds
from wikipedia_html_parsing import obtain_info_from_page

from datetime import datetime

import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure 'backend' is in sys.path so Python can find 'myproject'
sys.path.insert(0, BASE_DIR)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

from app.models import Wiki_Storms, Storm_Wiki_Data

#storms_with_quadrant_winds[i] = 

#[  {'Codename': 'AL012004',
#    'Name': 'ALEX', 
#    'Data': [
#   ['18510625', ' 0000', '  ', ' HU', ' 28.0N', '  94.8W', '  80', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510625', ' 0600', '  ', ' HU', ' 28.0N', '  95.4W', '  80', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510625', ' 1200', '  ', ' HU', ' 28.0N', '  96.0W', '  80', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510625', ' 1800', '  ', ' HU', ' 28.1N', '  96.5W', '  80', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'],
#   ['18510625', ' 2100', ' L', ' HU', ' 28.2N', '  96.8W', '  80', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510626', ' 0000', '  ', ' HU', ' 28.2N', '  97.0W', '  70', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510626', ' 0600', '  ', ' TS', ' 28.3N', '  97.6W', '  60', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'],
#   ['18510626', ' 1200', '  ', ' TS', ' 28.4N', '  98.3W', '  60', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510626', ' 1800', '  ', ' TS', ' 28.6N', '  98.9W', '  50', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510627', ' 0000', '  ', ' TS', ' 29.0N', '  99.4W', '  50', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510627', ' 0600', '  ', ' TS', ' 29.5N', '  99.8W', '  40', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510627', ' 1200', '  ', ' TS', ' 30.0N', ' 100.0W', '  40', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510627', ' 1800', '  ', ' TS', ' 30.5N', ' 100.1W', '  40', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999'], 
#   ['18510628', ' 0000', '  ', ' TS', ' 31.0N', ' 100.2W', '  40', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999', ' -999']
#   ]
#       }

# https://en.wikipedia.org/wiki/2005_Atlantic_hurricane_season#Tropical_Depression_Ten
# https://en.wikipedia.org/wiki/Tropical_Storm_Jose_(2005)
# https://en.wikipedia.org/wiki/Hurricane_Katrina

storm_names_year = [] 

classification_list = ['TD', 'TS', 'HU']

# TD tropical depression
# TS tropical storm
# HU tropical hurricane
# SD subtropical cyclone
# SS subtropical storm


#if only has TD as the highest could also be within https://en.wikipedia.org/wiki/2022_Atlantic_hurricane_season
def classify_storm(storm_data_block):
    print(f"storm_data_block {storm_data_block}")
    
    highest_classification = None  # Start as None
    valid_classifications = {
        'TD': 'Tropical_Depression',
        'TS': 'Tropical_Storm',
        'HU': 'Hurricane',
        'SD': 'Subtropical_Cyclone',
        'SS': 'Subtropical_Storm'
    }
    unknown_classifications = {'EX', 'LO', 'WV', 'DB'}  # Ignore these

    classification_hierarchy = {
        'Tropical_Depression': 1,
        'Subtropical_Cyclone': 2,
        'Subtropical_Storm': 3,
        'Tropical_Storm': 4,
        'Hurricane': 5
    }

    for line in storm_data_block:
        storm_type = line[3].strip()
        print(f"line: {line}, storm_type: {storm_type}")

        # Ignore unknown storm types
        if storm_type in unknown_classifications:
            print(f"Skipping unknown classification: {storm_type}")
            continue

        if storm_type in valid_classifications:
            classification = valid_classifications[storm_type]
            print(f"Found classification: {classification}")

            # If highest_classification is None, initialize it
            if highest_classification is None:
                highest_classification = classification
            # Compare classification levels
            elif classification_hierarchy[classification] > classification_hierarchy[highest_classification]:
                highest_classification = classification
                print(f"Updated highest_classification: {highest_classification}")

    # If no valid classification found, return 'UNKNOWN'
    return highest_classification if highest_classification else 'UNKNOWN'




def get_wikipedia_page(storm_dictionary):

    # wikipedia organises the storm urls by the following
    # https://en.wikipedia.org/wiki/Hurricane_Ian
    # https://en.wikipedia.org/wiki/Tropical_Storm_Alex_(2022), https://en.wikipedia.org/wiki/Hurricane_Bonnie_(2022),
    # https://en.wikipedia.org/wiki/2022_Atlantic_hurricane_season#Tropical_Storm_Colin, 
    # "https://en.wikipedia.org/wiki/Subtropical_Storm_Andrea(2007)",
    # "https://en.wikipedia.org/wiki/Subtropical_Cyclone_Andrea(2007)",
    # "https://en.wikipedia.org/wiki/Subtropical_Storm_Andrea",
    # "https://en.wikipedia.org/wiki/Subtropical_Cyclone_Andrea"

    if storm_dictionary['Classification'] == 'UNKNOWN':
        print(f"Unknown classification for URL, skipping for {storm_dictionary['Name']}")
        storm_dictionary['Url'] = 'UNKNOWN'
        return storm_dictionary

    base_url = "https://en.wikipedia.org/wiki/"


    possible_urls = [
        f"{base_url}{storm_dictionary['Classification']}_{storm_dictionary['Name']}_({storm_dictionary['Year']})", 
        f"{base_url}{storm_dictionary['Classification']}_{storm_dictionary['Name']}", 
        f"{base_url}{storm_dictionary['Year']}_Atlantic_hurricane_season#{storm_dictionary['Classification']}_{storm_dictionary['Name']}",
    ]

    for url in possible_urls:
        print(f"attempting url: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Url: {url} found.")
            storm_dictionary['Url'] = url
            return storm_dictionary  



    


for storm in storms_with_quadrant_winds:

    year = storm['Data'][0][0][:4]
    codename = storm['Codename']

    print(f"Attempting to obtain dictionary for storm {storm['Name']}")

    classification = classify_storm(storm['Data'])

    name_year_dict = {
        'Codename': codename,
        'Name': storm['Name'].capitalize(),
        'Year': year,
        'Classification': classification,
    }

    print(f"Dictionary is: {name_year_dict}")

    dict_with_url = get_wikipedia_page(name_year_dict)
    print(f"dict with url : {dict_with_url}")

    dict_with_all_info = {}

    if dict_with_url['Url'] != 'UNKNOWN':
        dict_with_all_info = obtain_info_from_page(dict_with_url)
        print(f"dict_with_all_info : {dict_with_all_info}")
    else:
        dict_with_all_info = dict_with_url
        print(f"dict_with_all_info : {dict_with_all_info}")

    #{'Name': 'Bonnie', 'Year': 2022, 'Classification': 'Hurricane', 'Url': 'https://en.wikipedia.org/wiki/Hurricane_Bonnie_(2022)', 
    #'Image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Bonnie_2022-07-05_1510Z.jpg/220px-Bonnie_2022-07-05_1510Z.jpg', 
    #'Formed': 'July 1, 2022', 'Dissipated': 'July 11, 2022', 'Fatalities': '5', 'Damage': '$25\xa0million (2022USD)', 
    #'Areas Affected': 'Trinidad and Tobago, Grenada, Venezuela,ABC Islands, Colombia,San Andres Island, Central America, Southwestern Mexico,Revillagigedo Islands'}


    # or {'Name': 'Bonnie', 'Year': 2022, 'Classification': 'Hurricane', 'Url': 'https://en.wikipedia.org/wiki/Hurricane_Bonnie_(2022)', 
    #'Image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Bonnie_2022-07-05_1510Z.jpg/220px-Bonnie_2022-07-05_1510Z.jpg', 
    # 'Duration': 'August 3 – August 14' 
    

    print(f"dict_with_all_info: {dict_with_all_info}")

    if dict_with_all_info:
       
        formed_date = dict_with_all_info.get('Formed', None) if dict_with_all_info.get('Formed', None) != 'Unknown' else None
        dissipated_date = dict_with_all_info.get('Dissipated', None) if dict_with_all_info.get('Dissipated', None) != 'Unknown' else None
        fatalities = dict_with_all_info.get('Fatalities', None)
        damage = dict_with_all_info.get('Damage', None)
        affected_areas = dict_with_all_info.get('Areas Affected', None)
        
        
        storm_wiki_data = Storm_Wiki_Data.objects.create(
            name=dict_with_all_info.get('Name', ''),
            formed_date=formed_date,
            dissipated_date=dissipated_date,
            classification=dict_with_all_info.get('Classification', ''),
            url=dict_with_all_info.get('Url', ''),
            image=dict_with_all_info.get('Image', ''),
            fatalities=fatalities,
            damage=damage,
            affected_areas=affected_areas
        )

    
    for line in storm['Data']:

        date_str = line[0].strip()  
        date_obj = datetime.strptime(date_str, '%Y%m%d').date() 

        #s is - , n is + . w is -, e is +

        latitude_str = line[4]
        if 'S' in latitude_str:
            latitude_int = -float(latitude_str.replace('S', ''))
        elif 'N' in latitude_str:
            latitude_int = float(latitude_str.replace('N', ''))

        longitude_str = line[5].strip()
        if 'W' in longitude_str:
            longitude_int = -float(longitude_str.replace('W', ''))
        elif 'E' in longitude_str:
            longitude_int = float(longitude_str.replace('E', ''))

        max_wind_str = line[6]
        max_wind_int = float(max_wind_str.strip())

        converted_strings = []

        for string in line[6:]:
            string_to_int = int(string.strip())
            converted_strings.append(string_to_int)

        radius_34 = float(converted_strings[1] + converted_strings[2] + converted_strings[3]) / 3
        radius_50 = float(converted_strings[4] + converted_strings[5] + converted_strings[6]) / 3
        radius_64 = float(converted_strings[7] + converted_strings[8] + converted_strings[9]) / 3

        wiki_storm = Wiki_Storms.objects.create(
            storm=storm_wiki_data,
            codename=name_year_dict['Codename'],
            date_YYYYMMDD=date_obj,
            latitude_n=latitude_int,
            longitude_w=longitude_int,
            maxwind_knots=max_wind_int,
            minimum_pressure_mb=converted_strings[0],
            NE_34kt=converted_strings[1],
            SE_34kt=converted_strings[2],
            SW_34kt=converted_strings[3],
            NW_34kt=converted_strings[4],
            NE_50kt=converted_strings[5],
            SE_50kt=converted_strings[6],
            SW_50kt=converted_strings[7],
            NW_50kt=converted_strings[8],
            NE_64kt=converted_strings[9],
            SE_64kt=converted_strings[10],
            SW_64kt=converted_strings[11],
            NW_64kt=converted_strings[12],
            radius_max_wind=max_wind_int,
            radius_34=radius_34,
            radius_50=radius_50,
            radius_64=radius_64
        )
    

    
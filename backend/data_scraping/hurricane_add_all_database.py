print("Executing the file hurricane_add_all_database.py")

import sys
import os
import math


from hurricane_scraping import storms_data



from datetime import datetime
import sys
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ensure 'backend' is in sys.path so Python can find 'myproject'
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

from app.models import AllStorms, StormOverview

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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # in kilometers




def classify_storm(storm_data_block):
    print(f"storm_data_block {storm_data_block}")
    
    highest_classification = None  
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

            if highest_classification is None:
                highest_classification = classification
            elif classification_hierarchy[classification] > classification_hierarchy[highest_classification]:
                highest_classification = classification
                print(f"Updated highest_classification: {highest_classification}")

    # If no valid classification found, return 'UNKNOWN'
    return highest_classification if highest_classification else 'UNKNOWN'



print(storms_data)



for storm in storms_data:
    print(f"Processing storm: {storm['Codename']}")  

    date_start_str = storm['Data'][0][0]
    date_end_str = storm['Data'][-1][0]

    date_start_obj = datetime.strptime(date_start_str, '%Y%m%d').date()
    date_end_obj = datetime.strptime(date_end_str, '%Y%m%d').date()

    codename = storm['Codename']
    storm_classification = classify_storm(storm['Data'])

    name_year_dict = {
        'Codename': codename,
        'Name': storm['Name'].capitalize(),
    }

    latitudes = []
    longitudes = []

    for idx, line in enumerate(storm['Data']):
        print(f"Processing line {idx}: {line}")  
        
        time_24hr = int(line[1].strip())

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

        max_wind = int(line[6].strip())

        min_pressure = line[7].strip()

        if min_pressure == '-999':
            min_pressure = None
        else:
            min_pressure = int(min_pressure)

        storm_in_all = AllStorms.objects.create(
            codename=name_year_dict['Codename'],
            time_24hr=time_24hr,
            date_start_YYYYMMDD=date_start_obj,
            date_end_YYYYMMDD=date_end_obj,
            latitude_n=latitude_int,
            longitude_w=longitude_int,
            maxwind_knots=max_wind,
            minimum_pressure_mb=min_pressure,
            current_classification=line[3].strip(),
            highest_classification=storm_classification
        )

        latitudes.append(latitude_int)
        longitudes.append(longitude_int)

        print(f"Current latitudes: {latitudes}")
        print(f"Current longitudes: {longitudes}")

        if idx == len(storm['Data']) - 1:
            print(f"Last entry for {storm['Codename']} reached, creating StormOverview.")  # Debug

            # Calculate the center (average latitude and longitude)
            center_lat = sum(latitudes) / len(latitudes)
            center_lon = sum(longitudes) / len(longitudes)

            # Calculate the maximum radius from the center for both latitude and longitude
            radius_from_centre_km = max(
                haversine(center_lat, center_lon, lat, lon) for lat, lon in zip(latitudes, longitudes)
            )

            print(f"codename: {codename}, year: {date_start_str[:4]}, centre_latitude_n:{center_lat}, centre_longitude_w: {center_lon}, radius_from_centre: {radius_from_centre_km}, highest_classification: {storm_classification}, name: {name_year_dict['Name']}")

            try:
                storm_overview_input = StormOverview.objects.create(
                    codename=name_year_dict['Codename'],
                    year=date_start_str[:4],  # Use the start year of the storm
                    centre_latitude_n=center_lat,
                    centre_longitude_w=center_lon,
                    radius_from_centre=radius_from_centre_km,
                    highest_classification=storm_classification,
                    name=name_year_dict['Name']
                )
                print(f"Created StormOverviewInput {storm_overview_input}.")
            except Exception as e:
                print(f"Error creating StormOverview: {e}")


            latitudes = []
            longitudes = []

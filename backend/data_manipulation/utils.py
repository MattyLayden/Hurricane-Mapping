from django.db import connection

from storm_classes import storm_entry

import psycopg2.extras  

# valid_classifications = {
#        'Tropical_Depression',
#        'Tropical_Storm',
#        'Hurricane',
#        'Subtropical_Cyclone',
#        'Subtropical_Storm'
#    }


def fetch_storm_data_from_db(connection, highest_classification):
    query = """
    SELECT id, codename, time_24hr, "date_start_YYYYMMDD", "date_end_YYYYMMDD", latitude_n, longitude_w,
           maxwind_knots, minimum_pressure_mb, current_classification, highest_classification
    FROM app_allstorms
    WHERE highest_classification = %s
    """
    #highest_classification is case sensitive
    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(query, (highest_classification,))
        rows = cursor.fetchall()
    
    return rows


#this is processing all of the storm data for analysis 
def process_storm_data(connection, highest_classification):
    storm_data = fetch_storm_data_from_db(connection, highest_classification)
    
    storm_entries = [
        storm_entry(
            row['codename'], row['time_24hr'], row['date_start_YYYYMMDD'],
            row['date_end_YYYYMMDD'], row['latitude_n'], row['longitude_w'],
            row['maxwind_knots'], row['minimum_pressure_mb'], row['current_classification'], row['highest_classification']
        )
        for row in storm_data
    ]
    
    return storm_entries



def fetch_wiki_storm_data_from_db(connection, highest_classification):
    query = """
    SELECT ws.id, ws.codename, ws."date_YYYYMMDD", ws.latitude_n, ws.longitude_w, ws.maxwind_knots, 
           ws.minimum_pressure_mb, ws.NE_34kt, ws.SE_34kt, ws.SW_34kt, ws.NW_34kt, 
           ws.NE_50kt, ws.SE_50kt, ws.SW_50kt, ws.NW_50kt, 
           ws.NE_64kt, ws.SE_64kt, ws.SW_64kt, ws.NW_64kt, 
           ws.radius_max_wind, ws.radius_34, ws.radius_50, ws.radius_64, 
           swd.id AS storm_id
    FROM app_wiki_storms ws
    LEFT JOIN app_storm_wiki_data swd ON ws.storm_id = swd.id
    WHERE ws.highest_classification = %s
    """

    #highest_classification is case sensitive

    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor: 
        cursor.execute(query, (highest_classification,))
        rows = cursor.fetchall()

    return rows


def process_wiki_storm_data(connection, highest_classification):
    wiki_storm_data = fetch_wiki_storm_data_from_db(connection, highest_classification)

    storm_entries = [
        {
            "storm_id": row['storm_id'],
            "codename": row['codename'],
            "date": row['date_YYYYMMDD'],
            "latitude_n": row['latitude_n'],
            "latitude_w": row['latitude_w'],
            "maxwind_knots": row['maxwind_knots'],
            "minimum_pressure_mb": row['minimum_pressure_mb'],
            "NE_34kt": row['NE_34kt'],
            "SE_34kt": row["SE_34kt"],
            "SW_34kt": row["SW_34kt"],
            "NW_34kt": row["NW_34kt"],
            "NE_50kt": row['NE_50kt'],
            "SE_50kt": row["SE_50kt"],
            "SW_50kt": row["SW_50kt"],
            "NW_50kt": row["NW_50kt"],
            "NE_64kt": row['NE_64kt'],
            "SE_64kt": row["SE_64kt"],
            "SW_64kt": row["SW_64kt"],
            "NW_64kt": row["NW_64kt"],
            "radius_max_wind": row['radius_max_wind'],
            "radius_34": row['radius_34'],
            "radius_50": row['radius_50'],
            "radius_64": row['radius_64']
        }
        for row in wiki_storm_data
    ]

    return storm_entries


def fetch_storm_wiki_data_from_db(connection, storm_id):
    query= """
    SELECT name, formed_date, dissipated_date, classification, url, image, fatalities, damage, affected_areas
    FROM app_storm_wiki_data
    WHERE storm_id = %s
    """

    #highest_classification is case sensitive

    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:  # Use DictCursor
        cursor.execute(query, (highest_classification,))
        rows = cursor.fetchall()

    return rows


    
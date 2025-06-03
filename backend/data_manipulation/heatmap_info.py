import sys
import os
import psycopg2


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils import process_storm_data  
#from backend.app.connection.local_connection import get_db_connection 

from django.db import connection


#connection = get_db_connection()

#request comes in: name of storm = Bonnie, year of storm = 2004

#path_coordinates(process_wiki_storm_data(connection, 'Tropical_Storm'))


def fetch_storm_by_name_and_year(name, year):
    query = """
    SELECT *
    FROM "app_storm_wiki_data"
    WHERE name = %s AND formed_date LIKE %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (name, f"%{year}"))
        return cursor.fetchall()


def fetch_corresponding_storm_entries(storm_id):
    query = """
    SELECT * 
    FROM "app_wiki_storms"
    WHERE storm_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (storm_id,))
        return cursor.fetchall()


def fetch_storm_by_year_codename(year, codename):
    query = """
    SELECT *
    FROM "app_allstorms"
    WHERE formed_date LIKE %s AND codename = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (storm_id,))
        return cursor.fetchall()



###################################################################

## special case when app_wiki_storm_data has no formed date
def fetch_codename_from_name_and_year(name, year):
    query = """
    SELECT codename
    FROM "app_stormoverview"
    WHERE name = %s AND year = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (name, year))
        return cursor.fetchall()

## special case when app_wiki_storm_data has no formed date

def fetch_wiki_storms_from_codename(codename):
    query = """
    SELECT *
    FROM "app_wiki_storms"
    WHERE codename = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (codename,))
        columns = [col[0] for col in cursor.description]  
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]  



def path_and_details_special_case(name, year):
    codename_result = fetch_codename_from_name_and_year(name, year)
    if not codename_result:
        return None

    codename = codename_result[0][0]
    wiki_entries = fetch_wiki_storms_from_codename(codename)
    classification_entries = fetch_times_classification_from_codename(codename)

    print(f"Classification entries is as follows... : {classification_entries}")

    if not wiki_entries or not classification_entries:
        return None

    if len(wiki_entries) != len(classification_entries):
        print("⚠️ Warning: Mismatched entry counts between wiki and classification.")

    enriched_entries = []
    for wiki_entry, classification in zip(wiki_entries, classification_entries):
        enriched_entry = wiki_entry.copy()
        enriched_entry['current_classification'] = classification.get('current_classification')
        enriched_entry['time_24hr'] = classification.get('time_24hr')
        enriched_entries.append(enriched_entry)

    return enriched_entries



###################################################################


def path_and_details(name, year):

    #needs to return storm type (for colour), latitude_n, longitude_w, 
    #and connected database information

    print(f"path and details function received name as : {name} and year as {year}")
    print(f"type for name is : {type(name)} and type for year is : {type(year)}")

    wiki_data_entry_tuples = fetch_storm_by_name_and_year(name, year)

    print(f"within path_and_details function, the wiki data tuples from fetch storm by name and year function is as follows {wiki_data_entry_tuples}")

    wiki_data_column_names = ['id', 'name', 'formed_date', 'dissipated_date', 'classification', 'url', 'image', 'fatalities', 'damage', 'affected_areas']

    storm_metadata = [dict(zip(wiki_data_column_names, entry)) for entry in wiki_data_entry_tuples]

    #checking multiple different possibilities of same name and year just in case
    # e.g. bonnie, 2004. checking if multiple bonnies occurred in 2004

    if len(wiki_data_entry_tuples) == 1:
        storm_ids = [int(wiki_data_entry_tuples[0][0])]
    else:
        storm_ids = [int(tup[0]) for tup in wiki_data_entry_tuples]

    storm_entries = []

    for storm_id in storm_ids:
        storm_entry = fetch_corresponding_storm_entries(storm_id)
        storm_entries.extend(storm_entry)

    #wiki data entry tuple example
    #[
    #(8, 'Ivan', 'September 2, 2004'..... etc)
    #   ]

    #storm entry example
    #[
    #(  1, AL022004,  2004-08-03 ,          12.9 ,       53.6, ... etc)
    #]
    #

    column_names = ['id', 'codename', 'date', 'latitude_n', 'longitude_w', 'maxwind_knots', 'minimum_pressure_mb', 'NE_34kt', 'SE_34kt', 'SW_34kt', 'NW_34kt', 'NE_50kt', 'SE_50kt', 'SW_50kt', 'NW_50kt', 'NE_64kt', 'SE_64kt', 'SW_64kt', 'NW_64kt', 'radius_max_wind', 'radius_34', 'radius_50', 'radius_64', 'storm_id']

    storm_entries_dicts = [dict(zip(column_names, entry)) for entry in storm_entries]

    response = {
        "meta_data": storm_metadata,
        "storm_entries": storm_entries_dicts
    }

    return response

print(path_and_details('Bonnie', '2004'))



def fetch_storms_by_year(year, storm_type):
    print(f"Fetch storms by year function running, storm types: {storm_type}")
    
    # If storm_type is empty, we return an empty list immediately
    if not storm_type:
        print("No storm types selected, returning empty result.")
        return []
    
    with connection.cursor() as cursor:
        # Create a series of OR conditions for each storm type (highest_classification)
        conditions = " OR ".join([f"highest_classification = %s" for _ in storm_type])
        query = f"""
        SELECT *
        FROM app_stormoverview
        WHERE year = %s AND ({conditions})
        """
        # Log the final query before execution
        print(f"Executing query: {cursor.mogrify(query, [year] + storm_type)}")
        cursor.execute(query, [year] + storm_type)
        
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results



def fetch_stormnames_by_year(year):
    query = """
    SELECT codename, name
    FROM "app_stormoverview"
    WHERE year = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (year,))
        rows = cursor.fetchall()

        storm_names = []
        for row in rows:
            storm_name = row[1]  #name
            if storm_name == "Unnamed":
                storm_name_and_codename = f"Unnamed - {row[0]}"
                storm_names.append(storm_name_and_codename)
            else:
                storm_names.append(storm_name)

        return storm_names


def fetch_times_classification_from_codename(codename):
    query = """
    SELECT current_classification, time_24hr
    FROM "app_allstorms"
    WHERE codename = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (codename,))
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]






###################################################################

## older storm fetching 

## fetch_codename_from_name_and_year(name, year)

## date_end_YYYYMMDD, latitude_n, longitude_w, maxwind_knots, minimum_pressure_mb, date_start_YYYYMMDD, current_classification, time_24hr

def fetch_older_storms_from_codename(codename):
    query = """
    SELECT "date_end_YYYYMMDD", "latitude_n", "longitude_w", "maxwind_knots",
           "minimum_pressure_mb", "date_start_YYYYMMDD", "current_classification", "time_24hr"
    FROM "app_allstorms"
    WHERE codename = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (codename,))
        columns = [col[0] for col in cursor.description]  
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]  



###################################################################

def fetch_predictions_as_dict(month):
    query = """
    SELECT *
    FROM predicted_storms
    WHERE month = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (month,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
import sys
import os


sys.path.append(os.path.abspath(os.path.dirname(__file__)))


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils import process_storm_data  
from backend.app.connection.local_connection import get_db_connection 



#need to sort out connection to db

################################ 

# USING SQL COMMAND SELECT DISTINCT highest_classification
# FROM "app_allstorms";

# highest_classification 
# ------------------------
# Hurricane
# Subtropical_Cyclone
# Tropical_Depression
# Tropical_Storm
# Subtropical_Storm


connection = get_db_connection()



def days_lasted_by_codename(classification_dataset):

    dictionary_codename_to_days = {}

    current_storm = classification_dataset[0].get_codename()

    for line in classification_dataset:

        if line.get_codename() != current_storm:
            current_storm = line.get_codename()
            print(f"New storm: {current_storm}")
            current_duration = line.calculate_duration()
            dictionary_codename_to_days[current_codename] = current_duration

        
    print(f"Dictionary created is : {dictionary_codename_to_days}")


#days_lasted_by_codename(process_storm_data(connection, 'Tropical_Storm'))


def frequency_by_year(classification_dataset):
    dictionary_year_to_frequency = {}

    
    current_year = classification_dataset[0].get_year()
    storms_in_year = set()

    for line in classification_dataset:
        codename = line.get_codename()
        year = line.get_year()

        
        if year != current_year:
            dictionary_year_to_frequency[current_year] = len(storms_in_year)
            storms_in_year.clear()  
            current_year = year  
        
       
        storms_in_year.add(codename)

   
    dictionary_year_to_frequency[current_year] = len(storms_in_year)

    return dictionary_year_to_frequency



#frequency_by_year(process_storm_data(connection, 'Tropical_Storm'))

def 

        
#def analyse_data():
#    connection = get_db_connection()

#    if connection is None:
#        print("Cannot obtain connection string from get_db_connection")
#        return None
    
#    try:
#        processed_tropical_depression_data = process_storm_data(connection, 'Tropical_Depression')
#        processed_tropical_storm_data = process_storm_data(connection, 'Tropical_Storm')
#        processed_hurricane_data = process_storm_data(connection, 'Hurricane')
#        processed_subtropical_cyclone_data = process_storm_data(connection, 'Subtropical_Cyclone')
#        processed_subtropical_storm_data = process_storm_data(connection, 'Subtropical_Storm')





#    except 
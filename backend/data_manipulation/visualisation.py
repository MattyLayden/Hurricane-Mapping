from utils import fetch_storm_data_from_db, process_storm_data


#line graphs for year x axis, number of storms y axis

def get_frequency_year_data(storm_type){

    storm_data = process_storm_data(storm_type)

    year_frequency = {}

    for entry in storm_data:
        codename = entry.get_codename()
        year = entry.get_year()

        if year not in year_frequency:
            year_frequency[year] = set()  

       
        year_frequency[year].add(codename)

   
    for year in year_frequency:
        year_frequency[year] = len(year_frequency[year])

   
    print(year_frequency)

}


def get_
from rest_framework.decorators import api_view
from rest_framework.response import Response

from data_manipulation.heatmap_info import path_and_details, fetch_storms_by_year, fetch_stormnames_by_year, path_and_details_special_case, fetch_codename_from_name_and_year, fetch_older_storms_from_codename, fetch_predictions_as_dict

# path_and_details is the function that connects to database (need try) and returns json of 
# {'meta_data': [{'id': 1, 'name': 'Bonnie', 'formed_date': 'August 3, 2004', 'dissipated_date': 'August 14, 2004', 'classification': 'Tropical_Storm', 'url': 'https://en.wikipedia.org/wiki/Tropical_Storm_Bonnie_(2004)', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/TS_Bonnie_11_aug_2004_1650Z.jpg/220px-TS_Bonnie_11_aug_2004_1650Z.jpg', 'fatalities': '3 direct, 1 indirect', 'damage': '$1.27\xa0million (2004USD)'}"}
# {'storm_entries': [{'id': 1, ... etc}.. {...}]

# path_and_details(name, year):

## this is a specific storm entry given a storm name and year

## /api/get_heatmap_storm_by_name_year/?year=1858&storm_name=Unnamed+-+AL061858
## or /api/get_heatmap_storm_by_name_year/?year=2020&storm_name=Hanna

@api_view(['GET'])
def get_map_storm_by_name_year_modern(request):
    storm_name = request.GET.get('storm_name')
    year = request.GET.get('year')

    if not storm_name or not year:
        return Response({"error": "Missing name or year"}, status=400)

    try:
        name_year_data = path_and_details(storm_name, year)

        print(f"api get_heatmap_storm_by_name_year, fetched data received: {name_year_data}")

        if (not name_year_data or not name_year_data.get('meta_data') or not name_year_data.get('storm_entries')):
            ## some storms from app_storm_wiki_data fetched via the path_and_details function can not find the correct storm as formed_date is not entered into the table.
            ##id  |  name   |  formed_date  | dissipated_date | classification |                             url                             |                                                           image                                                           |  fatalities   |         damage          |                         affected_areas                         
            ##232 | Chantal |               |                 | Tropical_Storm | https://en.wikipedia.org/wiki/Tropical_Storm_Chantal_(2019) | https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Chantal_2019-08-20_1420Z.jpg/250px-Chantal_2019-08-20_1420Z.jpg |               |                         | 

            name_year_data_special_case = path_and_details_special_case(storm_name, year)
            print(f"name year data special case function, in get heatmap storm name year api: returning - {name_year_data_special_case} ")
            if name_year_data_special_case:
                return Response({"data": name_year_data_special_case}, status=201)
            else:
                return Response({"error": "No storm data found for the given name and year."}, status=404)

        else:
            return Response({"data": name_year_data}, status=200)

    except Exception as e:
        print(f"500 Error in get_heatmap_storm_by_name_year API call: {e}")
        return Response({"error": "Internal server error"}, status=500)


## this is for overview - with a slider choosing the storms
##params: {year: yearSelection, storm_type: stormSelection,}

@api_view(['GET'])
def get_heatmap_storms_by_year(request):
    print(f"Request GET: {request.GET}")

    year = request.GET.get('year')
    storm_type = request.GET.getlist('storm_type[]')


    print(f"Storm type array on api side: {storm_type}")

    if not year:
        return Response({"error": "Missing year"}, status=400)

    try:
        storms_year_data = fetch_storms_by_year(year, storm_type)

        if not storms_year_data:
            return Response({"error": "No storm data found for the given year."}, status=404)
        else:
            # storms_year_data should be a dictionary like
            # {{"id": 1973, "codename": "AL212023", "year": 2023, "centre_latitude_n": 12.33, etc}}
            return Response({"data": storms_year_data}, status=200)

    except Exception as e:
        print(f"500 Error in get_heatmap_storms_by_year API call: {e}")
        return Response({"error": "Internal server error"}, status=500)


## this is for the autocomplete function within ByStorm component - obtaining name options from a user input of the year
@api_view(['GET'])
def get_stormnames_from_year(request):
    year = request.GET.get('year')

    if not year:
        return Response({"error": "No storm data found for the given year."}, status=400)

    try:
        stormnames_from_year = fetch_stormnames_by_year(year)

        if not stormnames_from_year:
            return Response({"error": "No storm names found for the given year"}, status=404)
        else:
            return Response({"data": stormnames_from_year}, status=200)

    except Exception as e:
        print(f"500 Error in get_stormnames_from_year API call: {e}")
        return Response({"error": "Internal server error"}, status=500)





## if Unnamed - AL051900, or year 2003 or before
## 
## fetch_codename_from_name_and_year(name, year)

##def fetch_older_storms_from_codename(codename):

@api_view(['GET'])
def get_map_storm_by_name_year_older(request):
    storm_name = request.GET.get('storm_name')
    year = request.GET.get('year')


    codename = None
    unnamed_label = None

    if storm_name.lower().startswith('unnamed'):
        parts = storm_name.split(' - ')
        print(f"Parts section : {parts}")
        if len(parts) == 2:
            unnamed_label = parts[0]  
            print(f"unnamed label section: {unnamed_label}")
            codename = parts[1]
            print(f"codename from parts section : {codename}")

    if not storm_name or not year:
        return Response({"error": "Missing name or year"}, status=400)

    try:
        if codename: 

            older_storms_data = fetch_older_storms_from_codename(codename)

            print(f"Older storms data from fetch storms by codename is : {older_storms_data}")

            if not older_storms_data:
                return Response({"error": "Error obtaining older storms data"}, status=404)
            else:
                return Response({"data":older_storms_data}, status=200)
        else:
            codename_fetched = fetch_codename_from_name_and_year(storm_name, year)
            
            print(f"codename fetched {codename_fetched}")
            if(codename_fetched):
                codename2 = codename_fetched[0][0]
                older_storms_data = fetch_older_storms_from_codename(codename2)

                if not older_storms_data:
                    return Response({"error": "Error obtaining older storms data"}, status=404)
                else:
                    return Response({"data":older_storms_data}, status=200)


    except Exception as e:
        print(f"500 Error in get_map_storm_by_name_year_older API call: {e}")
        return Response({"error": "Internal server error"}, status=500)
        


MONTH_NAME_TO_NUMBER = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12,
}

@api_view(['GET'])
def get_predictions_by_month(request):
    raw_month = request.GET.get('month')

    if not raw_month:
        return Response({'error': 'Month parameter is required.'}, status=400)

    # Convert month name to number if needed
    if raw_month.lower() in MONTH_NAME_TO_NUMBER:
        month = MONTH_NAME_TO_NUMBER[raw_month.lower()]
    else:
        try:
            month = int(raw_month)
            if not 1 <= month <= 12:
                raise ValueError
        except ValueError:
            return Response({'error': 'Month must be a valid name or number (1–12).'}, status=400)

    data = fetch_predictions_as_dict(month)
    return Response(data)

    
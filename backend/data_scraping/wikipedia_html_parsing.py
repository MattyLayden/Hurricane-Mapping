import requests
from bs4 import BeautifulSoup


def obtain_info_from_page(storm_dictionary_with_url):
    url = storm_dictionary_with_url.get('Url', None)
    if not url or url == "Unknown":
        print("Error: No valid URL found for this storm.")
        return None
    
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
    if response.status_code != 200:
        print(f"Failed to fetch data from URL: {url}, Status Code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")


    storm_details = {}

    #for single page pages, 
    # https://en.wikipedia.org/wiki/Hurricane_Ian
    # https://en.wikipedia.org/wiki/Tropical_Storm_Alex_(2022), https://en.wikipedia.org/wiki/Hurricane_Bonnie_(2022),

    table1 = soup.find("table", class_="infobox ib-weather-event") 

    #for https://en.wikipedia.org/wiki/2004_Atlantic_hurricane_season#Tropical_Storm_Bonnie
    # <tr> with classname infoxbox-data contains the date

    if not table1:
            print("Multiple storms detected. Checking individual storm tables.")
            tables = soup.find_all("table", class_="infobox")

            for table in tables:
                # Find the <a> tag containing the image
                link = table.find("a", class_="mw-file-description")
                
                if link:
                    # Print the 'href' of the link, which is the actual image file link
                    print(f"Link href: {link.get('href')}")
                    
                    # Check if the storm name and year are in the image link's href (not the text)
                    if storm_dictionary_with_url['Name'].lower() in link.get('href', '').lower() and str(storm_dictionary_with_url['Year']) in link.get('href', ''):
                        print(f"Found matching table for {storm_dictionary_with_url['Name']} {storm_dictionary_with_url['Year']}")
                        
                        # Find the image element
                        image = link.find("img", class_="mw-file-element")
                        if image and 'src' in image.attrs:
                            # Build the full image URL (ensure 'http' is added)
                            image_url = image['src'] if image['src'].startswith('http') else f"https:{image['src']}"
                            storm_dictionary_with_url['Image'] = image_url
                            print(f"Image URL: {storm_dictionary_with_url['Image']}")
                            return storm_dictionary_with_url
                else:
                    print("No link found in this table.")
            
            # If no matching table was found, return a warning or handle the situation
            print("No matching table found.")
            return None


   
    
    #class is mw-file-element src needs https:

    #getting single page table information

    image = table1.find("img", class_="mw-file-element")
    if image and 'src' in image.attrs:
        image_url = image['src'] if image['src'].startswith('http') else f"https:{image['src']}"
        storm_details['Image'] = image_url

    print("Searching for 'Formed'...")
    formed = table1.find("th", string=lambda text: text and "Formed" in text.strip())
    if formed:
        print(f"formed section: {formed}")
        formed_text = formed.find_next("td").get_text(strip=True)
        print(f"formed_text: {formed_text}")
        storm_details['Formed'] = formed_text
    else:
        print("Could not find 'Formed' in the table.")
        storm_details['Formed'] = 'Unknown'  # Ensure the key exists

    
    dissipated = table1.find("th", string="Dissipated")
    print(f"dissipated: {dissipated}")
    if dissipated:
        storm_details['Dissipated'] = dissipated.find_next("td").get_text(strip=True)
    
    category = table1.find("th", class_="infobox-header", string="Category 5 major hurricane")
    print(f"category: {category}")
    if category:
        storm_details['Category'] = category.get_text(strip=True)
    

    fatalities = table1.find("th", string="Fatalities")
    print(f"fatalities: {fatalities}")
    if fatalities:
        storm_details['Fatalities'] = fatalities.find_next("td").get_text(strip=True)

    damage = table1.find("th", string="Damage")
    print(f"damage: {damage}")
    if damage:
        storm_details['Damage'] = damage.find_next("td").get_text(strip=True)

    affected_areas = table1.find("th", string="Areas affected")
    print(f"affected areas: {affected_areas}")
    if affected_areas:
        storm_details['Areas Affected'] = affected_areas.find_next("td").get_text(strip=True)

    storm_dictionary_with_url.update(storm_details)

    return storm_dictionary_with_url



#storm_dictionary = {
#    'Name': 'Hurricane_Ian',
#   'Year': 2022,
#    'Url': 'https://en.wikipedia.org/wiki/Hurricane_Ian'
#}

#result = obtain_info_from_page(storm_dictionary)
#print(result)
    

#{'Name': 'Hurricane_Ian', 'Year': 2022, 'Url': 'https://en.wikipedia.org/wiki/Hurricane_Ian', 
#'Image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ian_2022-09-28_1256Z.jpg/220px-Ian_2022-09-28_1256Z.jpg', 
#'Formed': 'September 23, 2022', 'Dissipated': 'October 1, 2022',
# 'Category': 'Category 5 major hurricane', 'Fatalities': '161 (69 direct, 92 indirect)', 
#'Damage': '$112\xa0billion (2022USD)(Third-costliest tropical cycloneon record; costliest inFloridahistory)',
# 'Areas Affected': 'Trinidad and Tobago,Venezuela,Colombia,ABC islands,Jamaica,Cayman Islands,Cuba, SoutheastUnited States(especiallyFloridaandThe Carolinas)'}


#storm_dictionary = {
#    'Name': 'Hurricane_Bonnie',
#   'Year': 2022,
#    'Url': 'https://en.wikipedia.org/wiki/Hurricane_Bonnie_(2022)'
#}

#result = obtain_info_from_page(storm_dictionary)
#print(result)

#{'Name': 'Hurricane_Bonnie', 'Year': 2022, 'Url': 'https://en.wikipedia.org/wiki/Hurricane_Bonnie_(2022)', 
#'Image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Bonnie_2022-07-05_1510Z.jpg/220px-Bonnie_2022-07-05_1510Z.jpg', 
#'Formed': 'July 1, 2022', 'Dissipated': 'July 11, 2022', 'Fatalities': '5', 'Damage': '$25\xa0million (2022USD)', 
#'Areas Affected': 'Trinidad and Tobago, Grenada, Venezuela,ABC Islands, Colombia,San Andres Island, Central America, Southwestern Mexico,Revillagigedo Islands'}


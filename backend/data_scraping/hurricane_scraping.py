from bs4 import BeautifulSoup
import csv


with open("../../source_data/HURDAT.htm", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "lxml")


pre_tag = soup.find("pre")
if pre_tag:
    text_data= pre_tag.get_text()
else:
    text_data = ""


data_split_by_lines = text_data.strip().split("\n")

storms_data = []

i = 0

while i < len(data_split_by_lines):
    line = data_split_by_lines[i]
    #line when i=0 would look something like "AL011851, UNNAMED, 14,"
    #line when i=1 would look something like "18510625, 0000,  , HU, 28.0N,  94.8W,  80, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999"
    if line.startswith("AL"):
        parts = line.split(",")
        #line when i=0 ["AL011851, UNNAMED, 14"]
        storm_codename = parts[0].strip()
        storm_name = parts[1].strip()
        num_data_lines_in_block = int(parts[2].strip())

        storm_data ={
            'Codename': storm_codename,
            'Name': storm_name,
            'Data': []
        }

        for j in range(i+1, i+1+num_data_lines_in_block):
            data_parts = data_split_by_lines[j].split(",")
            storm_data['Data'].append(data_parts)

        storms_data.append(storm_data)

        i+=num_data_lines_in_block
    else:
        i+= 1

#print(storms_data)

#example of first storm data block

#[  {'Codename': 'AL011851',
#    'Name': 'UNNAMED', 
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


#storms_data holds the full set of data of hurricanes

#now going to create table storm data involving the quadrant winds (for displaying the area size)


filter_from = 'AL012004'

storms_with_quadrant_winds = []

start_filtering = False

for storm in storms_data:
    if start_filtering:
        storms_with_quadrant_winds.append(storm)
    if storm['Codename'] == filter_from:
        start_filtering = True

#print(storms_with_quadrant_winds)


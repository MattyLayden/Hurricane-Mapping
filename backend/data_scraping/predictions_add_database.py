

import pandas as pd
print("Executing the file predictions_add_database.py")

import sys
import os
import math


from hurricane_scraping import storms_data



from datetime import datetime
import sys
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

from app.models import PredictedStorm

columns = ['year', 'month', 'MEI', 'Predicted storm wind', 'Predicted storm radius(km)', 'Predicted storm Lat/Lon']

storms = [
    [2025, 1, 0.895813, '61.1 knots', '1298.5 km', (40.82, -63.12)],
    [2025, 4, 0.633083, '58.9 knots', '1911.1 km', (37.56, -42.28)],
    [2025, 5, -0.563908, '47.7 knots', '1078.9 km', (32.76, -75.70)],
    [2025, 6, -0.502292, '57.4 knots', '1940.8 km', (25.39, -74.37)],
    [2025, 7, -0.447408, '41.3 knots', '779.9 km', (32.55, -62.75)],
    [2025, 7, -0.447408, '48.4 knots', '2028.0 km', (25.94, -96.58)],
    [2025, 8, -0.398521, '67.2 knots', '3178.9 km', (25.46, -51.06)],
    [2025, 8, -0.398521, '50.5 knots', '2808.9 km', (21.79, -70.64)],
    [2025, 8, -0.398521, '45.3 knots', '2606.1 km', (35.31, -49.97)],
    [2025, 8, -0.398521, '130.0 knots', '2261.5 km', (25.26, -87.61)],
    [2025, 8, -0.398521, '114.8 knots', '934.6 km', (17.51, -40.90)],
    [2025, 9, -0.354976, '103.2 knots', '2500.2 km', (37.16, -52.13)],
    [2025, 9, -0.354976, '44.7 knots', '830.7 km', (29.45, -37.48)],
    [2025, 9, -0.354976, '71.8 knots', '3094.6 km', (19.26, -48.53)],
    [2025, 9, -0.354976, '57.6 knots', '1191.4 km', (29.22, -44.59)],
    [2025, 9, -0.354976, '91.3 knots', '4103.4 km', (32.57, -12.65)],
    [2025, 9, -0.354976, '66.8 knots', '1581.6 km', (23.54, -62.04)],
    [2025, 10, -0.316189, '87.0 knots', '2976.6 km', (27.10, -60.35)],
    [2025, 11, -0.281640, '75.2 knots', '1863.3 km', (26.80, -55.62)],
    [2025, 12, -0.250866, '63.1 knots', '1389.7 km', (31.29, -25.60)],
]


df_storms = pd.DataFrame(storms, columns=columns)


print(df_storms)



for _, row in df_storms.iterrows():
    PredictedStorm.objects.create(
        year=row['year'],
        month=row['month'],
        mei=row['MEI'],
        predicted_storm_wind=row['Predicted storm wind'],
        predicted_storm_radius_km=row['Predicted storm radius(km)'],
        latitude=row['Predicted storm Lat/Lon'][0],
        longitude=row['Predicted storm Lat/Lon'][1],
    )


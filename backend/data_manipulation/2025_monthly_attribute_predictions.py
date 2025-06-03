import pandas as pd


import sys
import os
import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.linear_model import LinearRegression
import calendar


# Project root = /Users/matthewlayden/Desktop/hurricanes
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))  # Add backend to path so 'app' is found

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')

import django
django.setup()

## time series predictions for Annual Anomalies

from app.models import EnrichedTimeseriesWithMei


def load_storm_data():
    qs = EnrichedTimeseriesWithMei.objects.filter(year__gte=1979)
    df = pd.DataFrame.from_records(qs.values(
        'year',
        'start_month',
        'mei',
        'annual_anomaly',
        'centre_latitude_n',
        'centre_longitude_w',
        'radius_from_centre',
        'highest_classification',
        'max_wind',
    ))
    df = df.rename(columns={'mei': 'avg_mei'})
    return df


def train_models_for_month(df, month):
    month_storms = df[df['start_month'] == month].copy()
    month_storms = month_storms.dropna(subset=[
        'avg_mei', 'annual_anomaly', 'max_wind',
        'radius_from_centre', 'centre_latitude_n', 'centre_longitude_w'
    ])
    n = len(month_storms)
    if n == 0:
        print(f" Warning: No data points available for month {month}. Skipping model training.")
        return None
    elif n < 3:
        print(f" Warning: Only {n} data points available for month {month}. Model may be unreliable.")

    X = month_storms[['avg_mei', 'annual_anomaly']]

    models = {
        'wind': LinearRegression().fit(X, month_storms['max_wind']),
        'radius': LinearRegression().fit(X, month_storms['radius_from_centre']),
        'lat': LinearRegression().fit(X, month_storms['centre_latitude_n']),
        'lon': LinearRegression().fit(X, month_storms['centre_longitude_w']),
    }

    return models


def predict_storm_attributes(models, mei, anomaly):
    
    X_new = pd.DataFrame({'avg_mei': [mei], 'annual_anomaly': [anomaly]})
    return {
        'max_wind': models['wind'].predict(X_new)[0],
        'radius_km': models['radius'].predict(X_new)[0],
        'latitude': models['lat'].predict(X_new)[0],
        'longitude': models['lon'].predict(X_new)[0],
    }


def predict_monthly_storm_attributes(month, mei, anomaly, storm_count=1):
    df = load_storm_data()
    models = train_models_for_month(df, month)
    
    print(f"for month {month} : this is the data")
    
    if models is None:
        print(f" No model available for month {month}. Skipping prediction.")
        return None
    
    month_storms = df[df['start_month'] == month].dropna(subset=[
        'avg_mei', 'annual_anomaly', 'max_wind',
        'radius_from_centre', 'centre_latitude_n', 'centre_longitude_w'
    ])

    if storm_count == 1:
        prediction = predict_storm_attributes(models, mei, anomaly)
        print(f"   ➤ Max Wind: {prediction['max_wind']:.1f} knots")
        print(f"   ➤ Radius:   {prediction['radius_km']:.1f} km")
        print(f"   ➤ Lat/Lon:  ({prediction['latitude']:.2f}, {prediction['longitude']:.2f})")
        return [prediction]
    else:
        predictions = predict_multiple_storms(models, mei, anomaly, storm_count, month_storms)
        for i, storm in enumerate(predictions, start=1):
            print(f"   Storm {i}:")
            print(f"     ➤ Max Wind: {storm['max_wind']:.1f} knots")
            print(f"     ➤ Radius:   {storm['radius_km']:.1f} km")
            print(f"     ➤ Lat/Lon:  ({storm['latitude']:.2f}, {storm['longitude']:.2f})")
        return predictions


def predict_multiple_storms(models, mei, anomaly, count, training_data):
    X_base = np.array([[mei, anomaly]])
  
    residuals = {
        'wind': training_data['max_wind'] - models['wind'].predict(training_data[['avg_mei', 'annual_anomaly']]),
        'radius': training_data['radius_from_centre'] - models['radius'].predict(training_data[['avg_mei', 'annual_anomaly']]),
        'lat': training_data['centre_latitude_n'] - models['lat'].predict(training_data[['avg_mei', 'annual_anomaly']]),
        'lon': training_data['centre_longitude_w'] - models['lon'].predict(training_data[['avg_mei', 'annual_anomaly']]),
    }
    stds = {k: residuals[k].std() for k in residuals}

    predictions = []
    for _ in range(count):
        pred = {
            'max_wind': models['wind'].predict(X_base)[0] + np.random.normal(0, stds['wind']),
            'radius_km': models['radius'].predict(X_base)[0] + np.random.normal(0, stds['radius']),
            'latitude': models['lat'].predict(X_base)[0] + np.random.normal(0, stds['lat']),
            'longitude': models['lon'].predict(X_base)[0] + np.random.normal(0, stds['lon']),
        }
        predictions.append(pred)
    return predictions



##    year start_month   avg_mei  annual_anomaly  predicted_storm_count
##0   2025           1 -0.895813        0.920391               1.104157
#1   2025           2 -0.797930        0.920391               1.092688
#2   2025           3 -0.710743        0.920391               1.082572
#3   2025           4 -0.633083        0.920391               1.566674
#4   2025           5 -0.563908        0.920391               1.354010
#5   2025           6 -0.502292        0.920391               1.868991
#6   2025           7 -0.447408        0.920391               2.476811
#7   2025           8 -0.398521        0.920391               4.784802
#8   2025           9 -0.354976        0.920391               5.786799
#9   2025          10 -0.316189        0.920391               3.276773
#10  2025          11 -0.281640        0.920391               1.516108
#11  2025          12 -0.250866        0.920391               1.292356

#so months: 1,2, 3,4, 5,6, 11, 12. are predicted as 1 storm

# month 1
month_1_attributes = predict_monthly_storm_attributes(
    month=1,
    mei=-0.895813,
    anomaly=0.920391
)

#   ➤ Max Wind: 61.1 knots
#   ➤ Radius:   1298.5 km
#   ➤ Lat/Lon:  (40.82, -63.12)


#######################


#month 2
month_2_attributes = predict_monthly_storm_attributes(
    month=2,
    mei=-0.797930,
    anomaly=0.920391
)

# not enough data for month 2
####################### 


#3
month_3_attributes = predict_monthly_storm_attributes(
    month=3,
    mei=-0.710743,
    anomaly=0.920391
)


# not enough data for month 3
####################### 


#4
month_4_attributes = predict_monthly_storm_attributes(
    month=4,
    mei=-0.633083,
    anomaly=0.920391
)


# ➤ Max Wind: 58.9 knots
#   ➤ Radius:   1911.1 km
#   ➤ Lat/Lon:  (37.56, -42.28)

####################### 



#5
month_5_attributes = predict_monthly_storm_attributes(
    month=5,
    mei=-0.563908,
    anomaly=0.920391
)

#   ➤ Max Wind: 47.7 knots
#   ➤ Radius:   1078.9 km
#   ➤ Lat/Lon:  (32.76, -75.70)


####################### 

#6
month_6_attributes = predict_monthly_storm_attributes(
    month=6,
    mei=-0.502292,
    anomaly=0.920391
)

#   ➤ Max Wind: 57.4 knots
#  ➤ Radius:   1940.8 km
#  ➤ Lat/Lon:  (25.39, -74.37)

####################### 

#7 
month_7_attributes = predict_monthly_storm_attributes(
    month=7,
    mei=-0.447408,
    anomaly=0.920391,
    storm_count=2
)

#   Storm 1:
    # ➤ Max Wind: 41.3 knots
    # ➤ Radius:   779.9 km
    #➤ Lat/Lon:  (32.55, -62.75)
  # Storm 2:
     #➤ Max Wind: 48.4 knots
     #➤ Radius:   2028.0 km
     #➤ Lat/Lon:  (25.94, -96.58)

####################### 


#8
month_8_attributes = predict_monthly_storm_attributes(
    month=8,
    mei=-0.398521,
    anomaly=0.920391,
    storm_count=5
)

#   Storm 1:
   #  ➤ Max Wind: 67.2 knots
    # ➤ Radius:   3178.9 km
    # ➤ Lat/Lon:  (25.46, -51.06)
   #Storm 2:
    # ➤ Max Wind: 50.5 knots
    # ➤ Radius:   2808.9 km
    # ➤ Lat/Lon:  (21.79, -70.64)
  # Storm 3:
    #➤ Max Wind: 45.3 knots
#   ➤ Radius:   2606.1 km
   #  ➤ Lat/Lon:  (35.31, -49.97)
  # Storm 4:
   #  ➤ Max Wind: 130.0 knots
    # ➤ Radius:   2261.5 km
    # ➤ Lat/Lon:  (25.26, -87.61)
  # Storm 5:
    # ➤ Max Wind: 114.8 knots
    # ➤ Radius:   934.6 km
    # ➤ Lat/Lon:  (17.51, -40.90)

####################### 


#9
month_9_attributes = predict_monthly_storm_attributes(
    month=9,
    mei=-0.354976,
    anomaly=0.920391,
    storm_count=6
)

  # Storm 1:
   #  ➤ Max Wind: 103.2 knots
   #  ➤ Radius:   2500.2 km
    # ➤ Lat/Lon:  (37.16, -52.13)
  # Storm 2:
   #  ➤ Max Wind: 44.7 knots
    # ➤ Radius:   830.7 km
    # ➤ Lat/Lon:  (29.45, -37.48)
  # Storm 3:
   #  ➤ Max Wind: 71.8 knots
   #  ➤ Radius:   3094.6 km
   #  ➤ Lat/Lon:  (19.26, -48.53)
  # Storm 4:
   #  ➤ Max Wind: 57.6 knots
    # ➤ Radius:   1191.4 km
    # ➤ Lat/Lon:  (29.22, -44.59)
  # Storm 5:
   #  ➤ Max Wind: 91.3 knots
   #  ➤ Radius:   4103.4 km
   #  ➤ Lat/Lon:  (32.57, -12.65)
  # Storm 6:
    # ➤ Max Wind: 66.8 knots
    # ➤ Radius:   1581.6 km
    # ➤ Lat/Lon:  (23.54, -62.04)

####################### 


#10
month_10_attributes = predict_monthly_storm_attributes(
    month=10,
    mei=-0.316189,
    anomaly=0.920391,
    storm_count=3
)


  # Storm 1:
   #  ➤ Max Wind: 87.0 knots
   #  ➤ Radius:   2976.6 km
   #  ➤ Lat/Lon:  (27.10, -60.35)
  # Storm 2:
   #  ➤ Max Wind: 74.7 knots
   #  ➤ Radius:   -7.0 km
   #  ➤ Lat/Lon:  (31.87, -69.26)
  # Storm 3:
   #  ➤ Max Wind: 105.8 knots
   #  ➤ Radius:   -30.8 km
   #  ➤ Lat/Lon:  (27.00, -89.36)

####################### 

#11
month_11_attributes = predict_monthly_storm_attributes(
    month=11,
    mei=-0.281640,
    anomaly=0.920391
)

   # ➤ Max Wind: 75.2 knots
   # ➤ Radius:   1863.3 km
   # ➤ Lat/Lon:  (26.80, -55.62)
####################### 


#12
month_12_attributes = predict_monthly_storm_attributes(
    month=12,
    mei=-0.250866,
    anomaly=0.920391
)

   #➤ Max Wind: 63.1 knots
  # ➤ Radius:   1389.7 km
  # ➤ Lat/Lon:  (31.29, -25.60)

####################### 


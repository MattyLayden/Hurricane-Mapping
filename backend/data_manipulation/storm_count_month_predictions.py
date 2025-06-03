import pandas as pd


import sys
import os
import pandas as pd
import statsmodels.api as sm
import numpy as np

# Project root = /Users/matthewlayden/Desktop/hurricanes
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))  # Add backend to path so 'app' is found

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')

import django
django.setup()

## time series predictions for Annual Anomalies

from app.models import StormCountsWithPredictors

qs = StormCountsWithPredictors.objects.filter(year__gt=1977).values()


df = pd.DataFrame.from_records(qs)

# Optional: display it
print(df)


#from anomaly_predictions import prediction_2025_anomaly

anomaly_prediction_2025 = 0.920390733590498

##Forecast for next 12 months:
##2025-01-01   -0.895813
#2025-02-01   -0.797930
#2025-03-01   -0.710743
#2025-04-01   -0.633083
#2025-05-01   -0.563908
#2025-06-01   -0.502292
#2025-07-01   -0.447408
#2025-08-01   -0.398521
#2025-09-01   -0.354976
#2025-10-01   -0.316189
#2025-11-01   -0.281640
#2025-12-01   -0.250866


mei_2025_monthly = [-0.895813, -0.797930, -0.710743, -0.633083, -0.563908, -0.502292, -0.447408, -0.398521, -0.354976, -0.316189, -0.281640, -0.250866]
anomaly_2025_monthly = [anomaly_prediction_2025]*12

df_2025 = pd.DataFrame({
    'year': [2025]*12,
    'start_month': list(range(1, 13)),
    'avg_mei': mei_2025_monthly,
    'annual_anomaly': anomaly_2025_monthly
})

df['avg_mei'] = pd.to_numeric(df['avg_mei'], errors='coerce')
df['annual_anomaly'] = pd.to_numeric(df['annual_anomaly'], errors='coerce')
df_2025['avg_mei'] = pd.to_numeric(df_2025['avg_mei'], errors='coerce')
df_2025['annual_anomaly'] = pd.to_numeric(df_2025['annual_anomaly'], errors='coerce')


df['start_month'] = df['start_month'].astype('category')
df_2025['start_month'] = df_2025['start_month'].astype('category')

X = pd.get_dummies(df[['avg_mei', 'annual_anomaly', 'start_month']], drop_first=True)
X = sm.add_constant(X, has_constant='add')


bool_cols = X.select_dtypes(include=['bool']).columns
X[bool_cols] = X[bool_cols].astype(int)

y = df['storm_count']
y = pd.to_numeric(y, errors='coerce')

non_nan_idx = y.notna()
X = X.loc[non_nan_idx]
y = y.loc[non_nan_idx]

poisson_model = sm.GLM(y, X, family=sm.families.Poisson()).fit()
print(poisson_model.summary())

poisson_model = sm.GLM(y, X, family=sm.families.Poisson()).fit()
print(poisson_model.summary())

X_2025 = pd.get_dummies(df_2025[['avg_mei', 'annual_anomaly', 'start_month']], drop_first=True)
X_2025 = sm.add_constant(X_2025, has_constant='add')

missing_cols = set(X.columns) - set(X_2025.columns)
for col in missing_cols:
    X_2025[col] = 0

bool_cols_2025 = X_2025.select_dtypes(include=['bool']).columns
X_2025[bool_cols_2025] = X_2025[bool_cols_2025].astype(int)

X_2025 = X_2025[X.columns]

df_2025['predicted_storm_count'] = poisson_model.predict(X_2025)
print(df_2025[['year', 'start_month', 'avg_mei', 'annual_anomaly', 'predicted_storm_count']])
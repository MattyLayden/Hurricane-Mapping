

import pandas as pd


import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# Project root = /Users/matthewlayden/Desktop/hurricanes
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))  # Add backend to path so 'app' is found

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')

import django
django.setup()

## time series predictions for Annual Anomalies

from app.models import SeaSurfaceTemperature


qs = SeaSurfaceTemperature.objects.all().order_by('year')
df = pd.DataFrame.from_records(qs.values('year', 'annual_anomaly'))


print(df.head())

df = df.sort_values("year")
df.set_index("year", inplace=True)


series = df["annual_anomaly"].copy()


#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
#import matplotlib.pyplot as plt

#plt.figure(figsize=(12, 5))

#plt.subplot(1, 2, 1)
#plot_acf(series, lags=20, ax=plt.gca())
#plt.title("ACF - Autocorrelation Function")

#plt.subplot(1, 2, 2)
#plot_pacf(series, lags=20, ax=plt.gca(), method='ywm')  # 'ywm' is usually stable
#plt.title("PACF - Partial Autocorrelation Function")

#plt.tight_layout()
#plt.show()



forecast_years = []
forecast_values = []


current_year = series.index.max()

for i in range(5):
    
    model = ARIMA(series, order=(3, 1, 0))  
    model_fit = model.fit()

    
    forecast = model_fit.forecast(steps=1)
    next_value = forecast.iloc[0]

    
    current_year += 1
    series.loc[current_year] = next_value

   
    forecast_years.append(current_year)
    forecast_values.append(next_value)




prediction_2025_anomaly = forecast_values[1]

plt.figure(figsize=(10, 5))
plt.plot(df.index, df["annual_anomaly"], label="Historical", marker='o')
plt.plot(forecast_years, forecast_values, label="Forecast (Next 5 Years)", marker='x', linestyle='--', color='red')
plt.xlabel("Year")
plt.ylabel("Annual Anomaly")
plt.title("Recursive Forecast of Sea Surface Temperature Anomaly (Next 5 Years)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

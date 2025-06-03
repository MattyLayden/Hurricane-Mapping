import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX  


def load_data():
    path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_scraping'))
    if path_to_add not in sys.path:
        sys.path.append(path_to_add)
    from mei_add_to_database import df
    print("Columns in df:", df.columns.tolist())
    return df


def preprocess_data(df):
    df_long = df.melt(id_vars=['Year'], value_vars=[str(i) for i in range(1, 13)],
                      var_name='month', value_name='mei')

    df_long['month'] = df_long['month'].astype(int)
    df_long['date'] = pd.to_datetime(dict(year=df_long['Year'], month=df_long['month'], day=1))
    df_long.set_index('date', inplace=True)
    df_long.sort_index(inplace=True)

    return df_long['mei']


def plot_acf_pacf(series, lags=36):
    plt.figure(figsize=(14, 6))
    plt.subplot(121)
    plot_acf(series, lags=lags, ax=plt.gca())
    plt.title('Autocorrelation Function (ACF)')

    plt.subplot(122)
    plot_pacf(series, lags=lags, ax=plt.gca(), method='ywm')
    plt.title('Partial Autocorrelation Function (PACF)')

    plt.tight_layout()
    plt.show()


def main():
    df = load_data()
    series = preprocess_data(df)

    
    model = SARIMAX(series, order=(1, 0, 1), seasonal_order=(0, 0, 0, 12))
    results = model.fit(disp=False)
    
    print(results.summary())  
    
    
    fitted_values = results.predict(start=series.index[0], end=series.index[-1])
    print("Fitted values (in-sample predictions):")
    print(fitted_values.head())  
    
    # Forecast next 12 months
    forecast_steps = 12
    forecast = results.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=series.index[-1] + pd.offsets.MonthBegin(),
                                   periods=forecast_steps, freq='MS')
    forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
    
    print(f"\nForecast for next {forecast_steps} months:")
    print(forecast_series)
    
   
    conf_int = forecast.conf_int()
    plt.figure(figsize=(10,6))
    plt.plot(series, label='Observed')
    plt.plot(fitted_values, label='Fitted')
    plt.plot(forecast_series, label='Forecast', color='red')
    plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)
    plt.legend()
    plt.title('MEI SARIMA Model - Fitted and Forecasted Values')
    plt.show()



if __name__ == "__main__":
    main()




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

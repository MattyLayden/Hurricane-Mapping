# Hurricane-Mapping

## Hurricane Mapping

Please find a 3 minute showcase here (Youtube Link via thumbnail):

[![Watch the video](https://img.youtube.com/vi/NKFy-NGPxcw/hqdefault.jpg)](https://youtu.be/NKFy-NGPxcw)

[https://img.youtube.com/vi/NKFy-NGPxcw/hqdefault.jpg)](https://youtu.be/NKFy-NGPxcw](https://youtu.be/NKFy-NGPxcw)

## Introduction

The main idea behind this project was to translate a large and complex data set (https://www.aoml.noaa.gov/hrd/hurdat/hurdat2.html) which contained 57229 lines of every storm entry recorded since 1851 to present, into a user friendly application that would best display the impact of climate change on frequency and sizes of hurricanes in the USA.

<img src="https://github.com/user-attachments/assets/25dbcbe4-c16a-43ec-8eec-f27188462128" alt="Hurricane Map" width="600"/>

## Tech stack:
**Backend & Analysis:**

Python (Pandas, NumPy, Statsmodels, BeautifulSoup), PostgreSQL, SQL, ARIMA/SARIMA time series modelling

Django

Matplotlib


**Frontend:**

React.Js, JavaScript, Leaflet.js for mapping

## Initial strategy

The dataset contained numerous incomplete entries, with the value **-999** used to denote missing data. I cleaned the data in my scripts to ensure that only relevant information was added to the database. The quality of the data also varied over time: from **1851 to 2004**, only basic storm information was available. However, starting in **2004**, more detailed entries were introduced, including wind direction at each storm point, as well as additional metadata such as fatalities and estimated costs sourced from Wikipedia.

To create meaningful visualizations, I structured the database in **PostgreSQL** with separate but connected tables to efficiently organize different types of information:

**Storm index**: A table listing each storm entry along with its codename or official storm name.

**Storm overview**: Including calculated storm centers, classifications, and reach, using geographical calculations (e.g., the Haversine formula).

**Recent storm metadata**: Additional information scraped from Wikipedia using Python's BeautifulSoup.

I linked these tables using shared identifiers such as storm name/codename and year, ensuring the data remained accessible and ready for further analysis and visualization.

## Prediction modelling:

Predicting a hurricane's location and characteristics based on historical data is challenging due to the complex and dynamic nature of storm formation. However, to explore potential forecasting approaches, I focused on two primary influences:

- Sea Surface Temperature (SST) trends
- ENSO indices (El Nino-South Oscillation i.e. natural climate pattern)

To explore the relationship between climate variables and hurricane characteristics such as frequency, intensity, and track, I analyzed historical data to identify patterns that might inform future projections.

As part of this, I used time series models to predict future sea surface temperatures (SSTs) and ENSO (El Niño–Southern Oscillation) indices. The NOAA provided annual SST anomalies dating back to 1880, representing deviations relative to a long-term baseline average, serving as a strong indicator of long-term climate change. For instance, in 1904, the SST anomaly was -1.177°C, whereas in 2023, it reached +1.161°C. This historical dataset was formatted as a CSV Excel file:

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/1286d20d-2f42-4148-98a2-6fefabd54f08" />


The ENSO indices were already formulated as multivariate time series through the Multivariate ENSO Index (MEI), which combines multiple oceanic and atmospheric variables into a single index capturing complex climate interactions:


<img width="600" alt="Image" src="https://github.com/user-attachments/assets/7b8b4802-50b3-4feb-9973-62b30bbb8175" />


Originally, I planned to predict several years into the future to better understand climate change's impact. However, after using a time series model of **ARIMA(3,1,0)**, I found that longer-term predictions quickly lost accuracy, likely due to high variability and uncertainty inherent in climate time series. Therefore, I adjusted my approach to focus on just 1 year ahead (2025):

![Image](https://github.com/user-attachments/assets/d23a2f61-110a-49db-b6e0-49c579442453)

Since the ENSO indices already account for multi-year phase shifts, I modeled my data using **SARIMA(1,0,1)(0,0,0)[12].** This model includes a 12-month seasonal period but no seasonal AR or MA terms. Note that this data begins from 1979:

![Image](https://github.com/user-attachments/assets/acc54860-db81-4346-96aa-37f09c001f2b)

With monthly predictions for 2025 from both variables, I estimated the frequency of storms per month using a Poisson distribution based on historical storm counts. For regression analysis, any categorical variables such as hurricane classification were encoded into numerical values for regression analysis.

To predict monthly storm features, I first created a table by normalising and obtaining all relevant data, using SQL joins and other processing techniques. 

Finally, I applied a linear regression model to explore the relationships between ENSO and SST predictors and hurricane characteristics such as maximum wind speed, location and radius.






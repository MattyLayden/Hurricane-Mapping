# Hurricane-Mapping

Please find a 3 minute showcase here:

[![Watch the video](https://img.youtube.com/vi/NKFy-NGPxcw/hqdefault.jpg)](https://youtu.be/NKFy-NGPxcw)

The main idea behind this project was to translate a large and complex data set (https://www.aoml.noaa.gov/hrd/hurdat/hurdat2.html) which contained 57229 lines of every storm entry recorded since 1851 to present, into a user friendly application that would best display the impact of climate change on frequency and sizes of hurricanes in the USA.

<img src="https://github.com/user-attachments/assets/25dbcbe4-c16a-43ec-8eec-f27188462128" alt="Hurricane Map" width="600"/>


<u>**Initial strategy:**</u>

The dataset contained numerous incomplete entries, with the value **-999** used to denote missing data. I cleaned the data in my scripts to ensure that only relevant information was added to the database. The quality of the data also varied over time: from **1851 to 2004**, only basic storm information was available. However, starting in **2004**, more detailed entries were introduced, including wind direction at each storm point, as well as additional metadata such as fatalities and estimated costs sourced from Wikipedia.

To create meaningful visualizations, I structured the database in **PostgreSQL** with separate but connected tables to efficiently organize different types of information:

**Storm index**: A table listing each storm entry along with its codename or official storm name.

**Storm overview**: Including calculated storm centers, classifications, and reach, using geographical calculations (e.g., the Haversine formula).

**Recent storm metadata**: Additional information scraped from Wikipedia using Python's BeautifulSoup.

I linked these tables using shared identifiers such as storm name/codename and year, ensuring the data remained accessible and ready for further analysis and visualization.

**Prediction modelling:
**

Predicting a hurricane's location and characteristics based on historical data is challenging due to the complex and dynamic nature of storm formation. However, to explore potential forecasting approaches, I focused on two primary influences:

- Sea Surface Temperature (SST) trends
- ENSO indices (El Nino-South Oscillation i.e. natural climate pattern)

By analyzing the historical relationship between these climate variables and hurricane characteristics (such as frequency, intensity, and track), I aimed to uncover patterns that could inform projections of future storm behavior.

To attempt this, I predicted future sea surface temperatures and ENSO indicies. The NOAA provided annual anomalies of sea surface temperatures from 1880 which is the best indication of climate change. For example, 1904 an anomaly of -1.177 was recorded, however in 2023 an anomaly of +1.161 was recorded. This was data annually, from 1880, in the form of a CSV Excel file.

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/1286d20d-2f42-4148-98a2-6fefabd54f08" />


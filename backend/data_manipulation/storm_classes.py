from datetime import datetime

class storm_entry:
    def __init__(self, codename, time_24hr, date_start_YYYYMMDD, date_end_YYYYMMDD, latitude_n, longitude_w, maxwind_knots, current_classification, highest_classification, minimum_pressure_mb):
        self.codename = codename
        self.time_24hr = time_24hr
        self.date_start = date_start_YYYYMMDD
        self.date_end = date_end_YYYYMMDD
        self.latitude_n = latitude_n
        self.longitude_w = longitude_w
        self.highest_classification = highest_classification
        self.maxwind_knots = maxwind_knots
        self.minimum_pressure_mb = minimum_pressure_mb

    def get_codename(self):
        return self.codename

    def calculate_duration(self):
        start_date = datetime.strptime(str(self.date_start), "%Y-%m-%d")
        end_date = datetime.strptime(str(self.date_end), "%Y-%m-%d")
        return (end_date - start_date).days

    def get_coordinates(self):
        return self.latitude_n, self.longitude_w

    def get_max_wind(self):
        return self.maxwind_knots

    def get_time(self):
        return self.time_24hr

    def minimum_pressure(self):
        return self.minimum_pressure_mb

    def current_classification(self):
        return self.current_classification
    
    def highest_classification(self):
        return self.highest_classification

    def get_year(self):
        return self.date_start[:4]



class wiki_storm_entry:
    def __init__(self, storm_id, codename, date, latitude_n, longitude_w, maxwind_knots,
                 minimum_pressure_mb, NE_34kt, SE_34kt, SW_34kt, NW_34kt,
                 NE_50kt, SE_50kt, SW_50kt, NW_50kt,
                 NE_64kt, SE_64kt, SW_64kt, NW_64kt,
                 radius_max_wind, radius_34, radius_50, radius_64):
        self.storm_id = storm_id
        self.codename = codename
        self.date = date
        self.latitude_n = latitude_n
        self.longitude_w = longitude_w
        self.maxwind_knots = maxwind_knots
        self.minimum_pressure_mb = minimum_pressure_mb
        self.NE_34kt = NE_34kt
        self.SE_34kt = SE_34kt
        self.SW_34kt = SW_34kt
        self.NW_34kt = NW_34kt
        self.NE_50kt = NE_50kt
        self.SE_50kt = SE_50kt
        self.SW_50kt = SW_50kt
        self.NW_50kt = NW_50kt
        self.NE_64kt = NE_64kt
        self.SE_64kt = SE_64kt
        self.SW_64kt = SW_64kt
        self.NW_64kt = NW_64kt
        self.radius_max_wind = radius_max_wind
        self.radius_34 = radius_34
        self.radius_50 = radius_50
        self.radius_64 = radius_64

    def get_coordinates(self):
        return self.latitude_n, self.longitude_w

    def get_storm_id(self):
        return self.storm_id

    def get_codename(self):
        return self.codename

    def get_date(self):
        return self.date

    def get_max_wind(self):
        return self.maxwind_knots

    def get_minimum_pressure(self):
        return self.minimum_pressure_mb

    def get_wind_quadrants_34kt(self):
        return self.NE_34kt, self.SE_34kt, self.SW_34kt, self.NW_34kt

    def get_wind_quadrants_50kt(self):
        return self.NE_50kt, self.SE_50kt, self.SW_50kt, self.NW_50kt

    def get_wind_quadrants_64kt(self):
        return self.NE_64kt, self.SE_64kt, self.SW_64kt, self.NW_64kt

    def get_radius_max_wind(self):
        return self.radius_max_wind

    def get_radius_34(self):
        return self.radius_34

    def get_radius_50(self):
        return self.radius_50

    def get_radius_64(self):
        return self.radius_64





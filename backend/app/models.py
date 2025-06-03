from django.db import models

class Storm_Wiki_Data(models.Model):

    name = models.CharField(max_length=100)
    formed_date = models.CharField(max_length=50, null=True, blank=True) 
    dissipated_date = models.CharField(max_length=50, null=True, blank=True)  
    classification = models.CharField(max_length=50)
    url = models.CharField(max_length=300)
    image = models.CharField(max_length=300)
    fatalities = models.CharField(max_length=50, null=True, blank=True)  
    damage = models.CharField(max_length=200, null=True, blank=True)  
    affected_areas = models.TextField(null=True, blank=True)  


    def __str__(self):
        return f"{self.name} ({self.classification})"



class AllStorms(models.Model):

    codename = models.CharField(max_length=100)
    time_24hr= models.IntegerField(null=True, blank=True)
    date_start_YYYYMMDD = models.DateField(default="1851-01-01")
    date_end_YYYYMMDD = models.DateField()
    latitude_n = models.IntegerField()
    longitude_w = models.IntegerField()
    maxwind_knots = models.IntegerField()
    minimum_pressure_mb = models.IntegerField(null=True, blank=True)
    current_classification = models.CharField(max_length=50, default="UNKNOWN")
    highest_classification = models.CharField(max_length=50, default="UNKNOWN")



    def __str__(self):
        return self.codename


class Wiki_Storms(models.Model):
    storm = models.ForeignKey(Storm_Wiki_Data, on_delete=models.CASCADE, related_name="storm_lines", null=True)
    codename = models.CharField(max_length=100)
    date_YYYYMMDD = models.DateField()
    latitude_n = models.FloatField()
    longitude_w = models.FloatField()
    maxwind_knots = models.IntegerField()
    minimum_pressure_mb = models.IntegerField(null=True, blank=True)
    NE_34kt = models.IntegerField()
    SE_34kt = models.IntegerField()
    SW_34kt = models.IntegerField()
    NW_34kt = models.IntegerField()
    NE_50kt = models.IntegerField()
    SE_50kt = models.IntegerField()
    SW_50kt = models.IntegerField()
    NW_50kt = models.IntegerField()
    NE_64kt = models.IntegerField()
    SE_64kt = models.IntegerField()
    SW_64kt = models.IntegerField()
    NW_64kt = models.IntegerField()
    radius_max_wind = models.IntegerField()
    radius_34 = models.FloatField()
    radius_50 = models.FloatField()
    radius_64 = models.FloatField()


    def __str__(self):
        return self.codename


#DETAIL:  Failing row contains (1, AL011851, 1851, 28.842857142857138, -97.91428571428571, null, Hurricane, Unnamed).



class StormOverview(models.Model):
    codename = models.CharField(max_length=100)
    year = models.IntegerField()
    centre_latitude_n = models.FloatField()
    centre_longitude_w = models.FloatField()
    radius_from_centre = models.FloatField()
    highest_classification = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.codename}, {self.year})"



class SeaSurfaceTemperature(models.Model):
    year = models.PositiveIntegerField(unique=True)
    annual_anomaly = models.FloatField()

    def __str__(self):
        return f"{self.year}: {self.annual_anomaly}"


class MonthlyMEI(models.Model):
    year = models.PositiveIntegerField(unique=True)
    m1 = models.FloatField(null=True, blank=True)
    m2 = models.FloatField(null=True, blank=True)
    m3 = models.FloatField(null=True, blank=True)
    m4 = models.FloatField(null=True, blank=True)
    m5 = models.FloatField(null=True, blank=True)
    m6 = models.FloatField(null=True, blank=True)
    m7 = models.FloatField(null=True, blank=True)
    m8 = models.FloatField(null=True, blank=True)
    m9 = models.FloatField(null=True, blank=True)
    m10 = models.FloatField(null=True, blank=True)
    m11 = models.FloatField(null=True, blank=True)
    m12 = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'monthly_mei'


    def __str__(self):
        return f"MEI Year: {self.year}"


class StormCountsWithPredictors(models.Model):
    year = models.IntegerField(primary_key=True)
    start_month = models.IntegerField()
    storm_count = models.IntegerField()
    avg_mei = models.FloatField()
    annual_anomaly = models.FloatField()

    class Meta:
        db_table = 'storm_counts_with_predictors'
        managed = False
        unique_together = (('year', 'start_month'),)


class EnrichedTimeseriesWithMei(models.Model):
    codename = models.CharField(max_length=20)
    year = models.IntegerField()
    centre_latitude_n = models.FloatField()
    centre_longitude_w = models.FloatField()
    radius_from_centre = models.FloatField()
    highest_classification = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    annual_anomaly = models.FloatField()
    max_wind = models.IntegerField()
    start_month = models.IntegerField()
    mei = models.FloatField()

    class Meta:
        db_table = 'enriched_timeseries_with_mei'
        managed = False  


class PredictedStorm(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    mei = models.FloatField()
    predicted_storm_wind = models.CharField(max_length=20)  
    predicted_storm_radius_km = models.CharField(max_length=20)  
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'predicted_storms'  
        verbose_name = 'Predicted Storm'
        verbose_name_plural = 'Predicted Storms'

    def __str__(self):
        return f"Storm {self.year}-{self.month} at ({self.latitude}, {self.longitude})"
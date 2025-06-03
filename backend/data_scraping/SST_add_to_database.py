print("Executing SST_add_to_database.py")

import sys
import os
import pandas as pd

# Project root = /Users/matthewlayden/Desktop/hurricanes
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))  # Add backend to path so 'app' is found

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')

import django
django.setup()

from app.models import SeaSurfaceTemperature

csv_path = os.path.join(BASE_DIR, 'source_data', 'sea-surface-temp_fig-1 2.csv')
print("Loading CSV from:", csv_path)

df_sst = pd.read_csv(csv_path, encoding='latin1')
df_subset = df_sst[['Year', 'Annual anomaly']]

print("First 5 rows:")
print(df_subset.head())

for _, row in df_subset.iterrows():
    SeaSurfaceTemperature.objects.update_or_create(
        year=row['Year'],
        defaults={'annual_anomaly': row['Annual anomaly']}
    )

print("✅ Database update complete.")

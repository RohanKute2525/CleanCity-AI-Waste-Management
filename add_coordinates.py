from pathlib import Path
import pandas as pd
import random

BASE_DIR = Path(__file__).resolve().parent

files = list(BASE_DIR.rglob("hotspot_prediction.csv"))

if not files:
    print("❌ hotspot_prediction.csv not found.")
    exit()

file_path = files[0]

print("Dataset found:")
print(file_path)

df = pd.read_csv(file_path)

locations = [
    ("Pimpri", 18.6298, 73.7997),
    ("Akurdi", 18.5913, 73.7389),
    ("Wakad", 18.5590, 73.7868),
    ("Shivajinagar", 18.5074, 73.8077),
    ("Katraj", 18.4575, 73.8077),
    ("Kharadi", 18.5679, 73.9143),
    ("Hadapsar", 18.5089, 73.9259),
    ("Baner", 18.5590, 73.7868),
    ("Viman Nagar", 18.5679, 73.9143),
    ("Kothrud", 18.5074, 73.8077)
]

latitude = []
longitude = []

for _, row in df.iterrows():

    zone = str(row["zone"])

    matches = [
        item for item in locations
        if item[0].lower() == zone.lower()
    ]

    if matches:
        _, lat, lon = matches[0]
    else:
        _, lat, lon = random.choice(locations)

    lat += random.uniform(-0.008, 0.008)
    lon += random.uniform(-0.008, 0.008)

    latitude.append(round(lat, 6))
    longitude.append(round(lon, 6))

df["latitude"] = latitude
df["longitude"] = longitude

df.to_csv(file_path, index=False)

print()
print("✅ Coordinates added successfully!")
print()
print("Columns:")
print(df.columns.tolist())

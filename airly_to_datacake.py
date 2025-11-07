import requests
import json
import os
from dotenv import load_dotenv


AIRLY_API_KEY = os.getenv("AIRLY_API_KEY")
LAT = os.getenv("LAT")
LNG = os.getenv("LNG")
DATACAKE_URL = os.getenv("DATACAKE_URL")

# --- S1 ---
url = f"https://airapi.airly.eu/v2/measurements/nearest?lat={LAT}&lng={LNG}"
headers = {"apikey": AIRLY_API_KEY}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Error fetching Airly data:", response.text)
    exit()

data = response.json()

# --- S2 ---
current = data.get("current", {})
values = {item["name"]: item["value"] for item in current.get("values", [])}

payload = {
    "pm25": values.get("PM25"),
    "pm10": values.get("PM10"),
    "temperature": values.get("TEMPERATURE"),
    "humidity": values.get("HUMIDITY"),
    "pressure": values.get("PRESSURE")
}

print("sending payload to Datacake: ", payload)

# --- S3 ---
res = requests.post(DATACAKE_URL, json=payload)
if res.status_code == 200:
    print("Data sent successfully to Datacake")
else:
    print("Failed to send data: ", res.text)
#!/usr/bin/env python3
"""
Fetch weather data from Open-Meteo API for Minneapolis, MN.
Maintains a rolling 30-day window of daily weather observations.
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Minneapolis coordinates
LATITUDE = 44.98
LONGITUDE = -93.27
DATA_FILE = Path(__file__).parent.parent / "data" / "weather.json"

# Open-Meteo API endpoint (free, no API key required)
API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current_weather():
    """Fetch current weather data from Open-Meteo."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "timezone": "America/Chicago"
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "temperature_c": current["temperature_2m"],
        "humidity_pct": current["relative_humidity_2m"],
        "precipitation_mm": current["precipitation"]
    }


def load_existing_data():
    """Load existing weather data from JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(data):
    """Save weather data to JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def main():
    """Main function to fetch and store weather data."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Load existing data
    data = load_existing_data()

    # Check if we already have today's data (idempotent)
    existing_dates = {entry["date"] for entry in data}
    if today in existing_dates:
        print(f"Data for {today} already exists. Skipping.")
        return

    # Fetch new data
    print(f"Fetching weather data for {today}...")
    weather = fetch_current_weather()
    data.append(weather)

    # Keep only last 30 days
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    data = [entry for entry in data if entry["date"] >= cutoff]

    # Sort by date
    data.sort(key=lambda x: x["date"])

    # Save
    save_data(data)
    print(f"Saved: {weather}")
    print(f"Total entries: {len(data)}")


if __name__ == "__main__":
    main()

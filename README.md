# Minneapolis Weather Pipeline

A simple data engineering project that automatically collects and visualizes daily weather data for Minneapolis, MN.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  GitHub Actions │────▶│ Python Script│────▶│  JSON Data  │────▶│ GitHub Pages │
│  (Daily Cron)   │     │  (fetch.py)  │     │  (weather)  │     │  (Dashboard) │
└─────────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                               │
                               ▼
                        ┌─────────────┐
                        │ Open-Meteo  │
                        │  API (Free) │
                        └─────────────┘
```

## Features

- **Automated Data Collection**: GitHub Actions runs daily at 8 AM UTC
- **Free & Keyless**: Uses Open-Meteo API (no authentication required)
- **Rolling 30-Day Window**: Maintains recent data without unbounded growth
- **Idempotent**: Safe to run multiple times per day
- **Interactive Dashboard**: Visualizes temperature, humidity, and precipitation trends

## Data Collected

| Metric | Unit | Description |
|--------|------|-------------|
| Temperature | °C | Current temperature at 2m height |
| Humidity | % | Relative humidity at 2m height |
| Precipitation | mm | Current precipitation amount |

## Project Structure

```
├── .github/workflows/
│   └── fetch_weather.yml    # Scheduled GitHub Action
├── scripts/
│   └── fetch_weather.py     # Data fetching script
├── data/
│   └── weather.json         # Collected weather data
├── docs/
│   └── index.html           # Dashboard (GitHub Pages)
└── requirements.txt         # Python dependencies
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the fetch script
python scripts/fetch_weather.py
```

## Setup Your Own

1. Fork this repository
2. Enable GitHub Pages (Settings → Pages → Source: `main`, Folder: `/docs`)
3. The workflow will start collecting data automatically
4. View your dashboard at `https://<username>.github.io/<repo-name>/`

## Technologies

- **Python**: Data fetching and processing
- **GitHub Actions**: Scheduled automation
- **Open-Meteo API**: Free weather data source
- **Chart.js**: Data visualization
- **GitHub Pages**: Static hosting

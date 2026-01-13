import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
from dotenv import load_dotenv
import os

def get_station_id(location_query):
    """Find weather stations based on location name"""
    stations = {
        'new york': ('GHCND:USW00094728', 'New York'),
        'los angeles': ('GHCND:USW00023174', 'Los Angeles'),
        'chicago': ('GHCND:USW00094846', 'Chicago'),
        'houston': ('GHCND:USW00012960', 'Houston'),
        'phoenix': ('GHCND:USW00023183', 'Phoenix'),
        'philadelphia': ('GHCND:USW00013739', 'Philadelphia'),
        'miami': ('GHCND:USW00012839', 'Miami'),
        'seattle': ('GHCND:USW00024233', 'Seattle'),
        'boston': ('GHCND:USW00014739', 'Boston'),
        'denver': ('GHCND:USW00003017', 'Denver')
    }

    location_lower = location_query.lower()
    
    if location_lower in stations:
        return stations[location_lower], location_query.title()
    else:
        print(f"\nSorry, '{location_query}' not found in database.")
        print("Available cities:", ", ".join([city.title() for city in stations.keys()]))
        return None, None
    
def fetch_climate_data(station_id, start_year, end_year, token):
    """Fetch temp data over multiple years"""
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    headers = {
    'token': token
    }

    all_data = []

    print(f"Fetching data for station {station_id} from {start_year} to {end_year}")

    for year in range(start_year, end_year + 1):
        params = {
        'datasetid': 'GHCND',
        'datatypeid': 'TMAX',
        'stationid': station_id, 
        'startdate': f'{year}-01-01',
        'enddate': f'{year}-12-31',
        'limit': 1000,
        'units': 'standard'
    }
        print(f"Getting {year}")
        response = requests.get(url, headers=headers, params=params)
        if response.status_code==200:
            data = response.json()
            if 'results' in data:
                all_data.extend(data['results'])
                print(f"✓ ({len(data['results'])} records)")
            else:
                print("✗ No data")
        else:
            print(f"✗ Error {response.status_code}")

        time.sleep(.5)

    if all_data:
        return pd.DataFrame(all_data)
        print(f"\n[DEBUG] Total records: {len(df)}")
        print(f"[DEBUG] Sample dates:")
        print("bruh")
    else:
        print("Data not found")
        return None

def analyze_temperature(df, city_name, start_year, end_year):
    df['date'] = pd.to_datetime(df['date'])
    df['temp_f'] = df['value']

    stats = {
    'mean_temp': df['temp_f'].mean(),
    'max_temp': df['temp_f'].max(),
    'min_temp': df['temp_f'].min(),
    'std_temp': df['temp_f'].std(),
    'summer_avg': df[df['date'].dt.month.isin([6,7,8])]['temp_f'].mean(),
    'winter_avg': df[df['date'].dt.month.isin([12,1,2])]['temp_f'].mean()
    }

    plt.figure(figsize=(12,6))
    plt.plot(df['date'], df['temp_f'])
    plt.title(f"{city_name} Max Temperature")
    plt.xlabel("Date")
    plt.ylabel("Max Temperature (°F)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{city_name}_{start_year}-{end_year}", dpi=300)
    print(f"\n✓ Plot saved as {city_name}_{start_year}-{end_year}")

    return stats

def get_ai_analysis(stats, city_name, start_year, end_year):
    year_range = f"{start_year}-{end_year}" if start_year != end_year else str(start_year)
    years_text = f"{end_year - start_year + 1} years" if start_year != end_year else "one year"

    prompt = f"""You are a climate data analyst preparing a briefing on {city_name}'s temperature patterns based on {years_text} of data ({year_range}).

    TEMPERATURE STATISTICS:
    - Annual average: {stats['mean_temp']:.1f}°F
    - Highest recorded: {stats['max_temp']:.1f}°F
    - Lowest recorded: {stats['min_temp']:.1f}°F
    - Annual Range: {stats['max_temp'] - stats['min_temp']:.1f}°F
    - Summer average: {stats['summer_avg']:.1f}°F
    - Winter average: {stats['winter_avg']:.1f}°F
    - Variability: {stats['std_temp']:.1f}°F

Provide a comprehensive analysis covering:

1. **Climate Classification**: What Köppen climate type is this?
2. **Temperature Extremes**: How does the {stats['max_temp'] - stats['min_temp']:.1f}°F range compare nationally?
3. **Seasonal Contrast**: Interpret the {stats['summer_avg'] - stats['winter_avg']:.1f}°F summer-winter difference
4. **Weather Stability**: What does {stats['std_temp']:.1f}°F variability mean for daily weather?
5. **Living Conditions**: What should residents expect in terms of heating/cooling costs, clothing needs, and outdoor lifestyle?

Be specific and insightful. (8-10 sentences)"""

    print("Analysis:")

    try:

        response = requests.post('http://localhost:11434/api/generate', json = {
            'model':"llama3.2",
            'prompt':prompt,
            'stream':False,
        }, timeout=60)

        result = response.json()
        print(result['response'])
        print("="*60)
    except Exception as e: 
        print(f"Error connecting to Ollama: {e}")
        print("Make sure Ollama is running!")
        print("="*60)

def main():
    print("="*60)
    print("Climate Data Analysis")
    print("="*60)

    #input
    location = input("\nEnter city name (e.g., 'New York City'): ").strip() 
    start_year = input("Enter start year (e.g., 2023): ").strip()
    end_year = input("Enter end year (e.g., 2023): ").strip()

    try:
        start_year = int(start_year)
        end_year = int(end_year)

        if start_year < 2000 or end_year > 2024:
            print("Please enter years between 2000 and 2024")
            return 
        
        if start_year > end_year:
            print("Start year must be less than or equal to end year")
            return
    
    except ValueError: 
        print("Invalid year format")
        return 
    
    #getid
    station_id, city_name = get_station_id(location)
    if not station_id:
      return
    
    token = os.getenv('NOAA_API_TOKEN')
    if not token :
        print("NOAA API token not found. Please set the NOAA_API_TOKEN environment variable.")
        return 

    df = fetch_climate_data(station_id, start_year, end_year, token)
    if df is None:
        return 
    if df is None:
        print("No data returned!")
        return
    
    stats = analyze_temperature(df, city_name, start_year, end_year)
    
    get_ai_analysis(stats, city_name, start_year, end_year)

    year_text = f"{start_year}-{end_year}" if start_year != end_year else str(start_year)
    print(f"\nAnalysis complete for {city_name} ({year_text})")

if __name__ == "__main__":
    main()
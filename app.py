import openmeteo_requests
import requests
import requests_cache
import pandas as pd
import secrets

from flask import Flask, request, redirect, url_for, render_template, session
from retry_requests import retry # type: ignore
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

#BOILER PLATE OPEN METEO API CODE ___START____

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
# Initial params with dynamic latitude and longitude
params = {

    "latitude": None,  # Placeholder for dynamic latitude
    "longitude": None,  # Placeholder for dynamic longitude
    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "cloud_cover", "wind_speed_10m"],
    "hourly": ["temperature_2m", "weather_code", "cloud_cover_low"],
    "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code"],
    "timezone": "auto"
}

#BOILER PLATE OPEN METEO API CODE ___END____


# Default coordinates
DEFAULT_LATITUDE = 43.82939
DEFAULT_LONGITUDE = 18.30003

#Weather codes are used to dynamically change all of the icons on the website depending on the current/daily/hourly weather

weather_codes = {
    0: "Clear sky", 
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle (moderate)",
    57: "Freezing drizzle (heavy)",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Slight thunderstorm",
    96: "Moderate thunderstorm",
    99: "Thunderstorm with hail"
}

#Returns the latitude and longitude to the main flask function to be used in fetching the data in the BOILER PLATE CODE

def fetch_geolocation(city_name):
    #Fetches latitude and longitude for a given city name.
    GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    response = requests.get(GEOCODING_API, params=params)
    #print(f"Geolocation Response: {response.json()}")  # Debugging line to check the full response
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]
            
            return latitude, longitude,
        else:
            
            return None, None
    else:
        
        return None, None

#Updates the params in the BOILER PLATE CODE section to the match the geo location fetched latitude and longitude

def update_params_with_city(city_name):
    """Updates params with geolocation based on the city name."""
    global params  # Use the global params variable
    latitude, longitude = fetch_geolocation(city_name)

    # Use fetched coordinates or fallback to default values
    params["latitude"] = latitude if latitude is not None else DEFAULT_LATITUDE
    params["longitude"] = longitude if longitude is not None else DEFAULT_LONGITUDE
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    #print(f"Updated Params: {params}")  # Log the updated parameters
    return params,response

#Fetches the weather data based upon the updated parameters

def fetch_weather_data():
    """Fetch weather data dynamically based on updated params."""
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]  # Assuming single location
    return response

#Processes the current weather data and returns it to be displayed in HTML

def process_current_data(response):
    """Process current weather data."""
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_weather_code = current.Variables(3).Value()
    current_cloud_cover = current.Variables(4).Value()
    current_wind_speed_10m = current.Variables(5).Value()
    current_weather = weather_codes.get(current_weather_code, "Unknown weather")
    weather_code_img = f"{int(current_weather_code)}"
    
    return {
        "current_temp": int(current_temperature_2m),
        "humidity" : int(current_relative_humidity_2m),
        "current_cloud_cover" : int(current_cloud_cover),
        "wind_speed" : int(current_wind_speed_10m),
        "current_weather" : current_weather,
        "apparent" : int(current_apparent_temperature),
        "img" : weather_code_img,
    }

#Processes the hourly weather data returns it to be displayed in HTML

def process_hourly_data(response):
    """Process hourly weather data."""
    current_time = int(datetime.now().hour)
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
	    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = hourly.Interval()),
	    inclusive = "left"
    )}
    hourly_data["date"] = pd.Series(hourly_data["date"]).dt.strftime('%H:%M')
    hourly_data["temperature_2m"] = [int(temp) for temp in hourly_temperature_2m]
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hour1 = hourly_dataframe.iloc[current_time + 2]
    hour2 = hourly_dataframe.iloc[current_time + 3]
    hour3 = hourly_dataframe.iloc[current_time + 4]
    hour4 = hourly_dataframe.iloc[current_time + 5]
    hour5 = hourly_dataframe.iloc[current_time + 6]
    hour6 = hourly_dataframe.iloc[current_time + 7]
    hour7 = hourly_dataframe.iloc[current_time + 8]
    fog = hourly_cloud_cover_low[current_time + 1]
    #print(hour1['date'])
    #print(hour1['cloud_cover_low'])
    #print(hourly_cloud_cover_low)
    hourly_data = {
        "hour1" : hour1,
        "hour2" : hour2,
        "hour3" : hour3,
        "hour4" : hour4,
        "hour5" : hour5,
		"hour6" : hour6,
        "hour7" : hour7,
        "current_fog" : int(fog),
        "weather1" : weather_codes.get(hour1['weather_code'], "Unkown weather"),
        "weather2" : weather_codes.get(hour2['weather_code'], "Unkown weather"),
        "weather3" : weather_codes.get(hour3['weather_code'], "Unkown weather"),
		"weather4" : weather_codes.get(hour4['weather_code'], "Unkown weather"),
    	"weather5" : weather_codes.get(hour5['weather_code'], "Unkown weather"),
        "weather6" : weather_codes.get(hour6['weather_code'], "Unkown weather"),
        "weather7" : weather_codes.get(hour7['weather_code'], "Unkown weather"),
        #"time" : current_time,
        "img1" : f"{int(hourly_weather_code[current_time + 2])}",
        "img2" : f"{int(hourly_weather_code[current_time + 3])}",
        "img3" : f"{int(hourly_weather_code[current_time + 4])}",
        "img4" : f"{int(hourly_weather_code[current_time + 5])}",
        "img5" : f"{int(hourly_weather_code[current_time + 6])}",
        "img6" : f"{int(hourly_weather_code[current_time + 7])}",
        "img7" : f"{int(hourly_weather_code[current_time + 8])}",
    }
    
    return hourly_data


#Processes weekly names to be displyed dynamically in HTML depending on the upcoming days. It is displayed in the Weekly forecast section. 

def get_day_names():
    today = datetime.now()
    day_names = [(today + timedelta(days=i)).strftime('%A') for i in range(7)]
    print(day_names)
    return{
        "day_tomorrow" : day_names[1],
        "day_tomorrow1" : day_names[2],
        "day_tomorrow2" : day_names[3],
        "day_tomorrow3" : day_names[4],
        "day_tomorrow4" : day_names[5],
    }
    

#processes the daily weather data and returns it to be displayed in HTML. 

def process_daily_data(response):
    """Process daily weather data."""

    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_weather_code = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
	    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = daily.Interval()),
	    inclusive = "left"
    )}

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["weather_code"] = daily_weather_code

    daily_dataframe = pd.DataFrame(data = daily_data)
    print(daily_dataframe)
    #print(daily_weather_code)
    
    #print(daily_temperature_2m_max)
    return {
        "tomorrow_weather" : weather_codes.get(daily_weather_code[2], "Unknown weather"),
        "tomorrow_weather1" : weather_codes.get(daily_weather_code[3], "Unknown weather"),
        "tomorrow_weather2" : weather_codes.get(daily_weather_code[4], "Unknown weather"),
        "tomorrow_weather3" : weather_codes.get(daily_weather_code[5], "Unknown weather"),
        "tomorrow_weather4" : weather_codes.get(daily_weather_code[6], "Unknown weather"),
        "img1_tomorrow" : int(daily_weather_code[2]),
        "img2_tomorrow" : int(daily_weather_code[3]),
        "img3_tomorrow" : int(daily_weather_code[4]),
        "img4_tomorrow" : int(daily_weather_code[5]),
        "img5_tomorrow" : int(daily_weather_code[6]),
        "max_temp" : int(daily_temperature_2m_max[1]),
        "min_temp" : int(daily_temperature_2m_min[1]),
        
    }

#Main Flask code that engages on first load and after that every time when somebody enters a town name

@app.route('/', methods=["GET", "POST"])
def home():
    
    global params

    weather_data = {}
    hourly_data = {}
    daily_data = {}
    city_name = "Ilidža"  # Fallback city name

    if request.method == "POST":
        city_name = request.form.get("town_name", "Ilidža")
        latitude, longitude = fetch_geolocation(city_name)
        params["latitude"] = latitude if latitude is not None else DEFAULT_LATITUDE
        params["longitude"] = longitude if longitude is not None else DEFAULT_LONGITUDE
        
        if params["latitude"] == DEFAULT_LATITUDE and  params["longitude"]  == DEFAULT_LONGITUDE :
            city_name = "Ilidža"
    
    else:
        # On first load, set the params to default for "Ilidža"
        params["latitude"] = DEFAULT_LATITUDE
        params["longitude"] = DEFAULT_LONGITUDE
        

    response = fetch_weather_data()
    weather_data = process_current_data(response)
    hourly_data = process_hourly_data(response)
    daily_data = process_daily_data(response)
    day_names = get_day_names()
    return render_template(
        "index.html",
        **weather_data,
        **hourly_data,
        **daily_data,
        **day_names,
        town_name=city_name.title(),
        
    )

if __name__ == '__main__':
    app.run(debug=True)



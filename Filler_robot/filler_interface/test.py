import os
import requests
from geopy.geocoders import Nominatim
import requests

# Get the user's current location
geolocator = Nominatim(user_agent="MyApp")
location = geolocator.geocode("My Location")
latitude = location.latitude
longitude = location.longitude

# Make a request to the Dark Sky API
url = "https://api.darksky.net/forecast/YOUR_API_KEY/LATITUDE,LONGITUDE"
url = url.replace("YOUR_API_KEY", os.getenv("DARK_SKY_API_KEY"))
url = url.replace("LATITUDE", str(latitude))
url = url.replace("LONGITUDE", str(longitude))
response = requests.get(url)

# Parse the response
data = response.json()
weather = data["currently"]["summary"]
temperature = data["currently"]["temperature"] - 273.15  # Convert from Kelvin to Celsius

# Print the weather forecast
print(f"The weather in your location is currently {weather} with a temperature of {temperature:.2f} degrees Celsius.")
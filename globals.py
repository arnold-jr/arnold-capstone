import os

# Read in all API keys from environment
google_api_key = os.environ['GOOGLE_SERVER_API_KEY']
google_geocode_api_key = os.environ['GOOGLE_GEOCODE_API_KEY']
cartodb_api_key = os.environ['CARTODB_API_KEY']

# define amenity types
AMENITY_TYPES = ['bakery',
 'bar',
 'cafe',
 'grocery_or_supermarket',
 'movie_theater',
 'park',
 'pharmacy',
 'restaurant',
 'school',
 'spa',
 'subway_station']

# Define dict for outputting names
DISPLAY_NAMES = {
    "SALEPRICE" : "last sale price",
    "bakery" : "bakeries",
    "bar" : "bars",
    "cafe" : "cafes",
    "grocery_or_supermarket" : "grocery stores",
    "movie_theater" : "movie theaters",
    "park" : "parks",
    "pharmacy" : "pharmacies",
    "restaurant" : "restaurants",
    "school" : "schools",
    "spa" : "spas",
    "subway_station" : "metro stations"
    }

with open('./data/valid_zipcodes.txt','r') as f:
    VALID_ZIPCODES = [line.strip() for line in f.readlines()]

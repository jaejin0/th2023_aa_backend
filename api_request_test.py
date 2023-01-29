from api_keys import *
import requests
import geocoder
from datetime import date, datetime
from zoneinfo import ZoneInfo

def get_flights_info(year, month, day, flight_number):
    headers = {}
    payload = {}
    url = f"http://localhost:4000/flights?date={year}-{month}-{day}"
    response = requests.get(url, headers=headers, data=payload)
    readable_response = response.json()

    for response in readable_response:
        if response["flightNumber"] == flight_number:
            origin = str(response["origin"])
            origin_list = origin.split(",")[1]
            origin_name = origin_list.split(":")[1][2:-1] # return value

            destination = str(response["destination"])
            destination_list = destination.split(",")[1]
            dest_name = destination_list.split(":")[1][2:-1] # return value

            timezone_list = origin.split(",")[2]
            timezone_name = timezone_list.split(":")[1][2:-1]
            leave_time = str(response["departureTime"])
            time_formated = datetime.strptime(leave_time, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo(timezone_name)).strftime('%I:%M %p') # return value

            first_coords = str(response["origin"])
            coords_list = first_coords.split(",")[3:5]
            air_latitude = coords_list[0].split(":")[2] # return value
            air_longitude = coords_list[1].split(":")[-1].strip("{}") # return value

            g = geocoder.ip('me')
            user_lat = g.latlng[0]
            user_long = g.latlng[-1]

            travel_time = get_maps_info(user_lat, user_long, air_latitude, air_longitude)

            return origin_name, dest_name, time_formated, air_latitude, air_longitude, user_lat, user_long, travel_time
            # must return destination and originand departure time


def get_maps_info(origin_lat, origin_long, airport_lat, airport_long):
    headers = {}
    payload = {}

    origin_list = []
    origin_lat = str(origin_lat)
    origin_long = str(origin_long)
    origin_list.append(origin_lat)
    origin_list.append(origin_long)

    for coord in origin_list:
        if float(coord) < 0:
            coord = f"+{coord[0][1:]}"
    origin_lat = origin_list[0].strip()
    origin_long = origin_list[1].strip()

    airport_list = []
    airport_list.append(airport_lat)
    airport_list.append(airport_long)

    for air_coord in airport_list:
        if float(air_coord) < 0:
            air_coord = f"+{air_coord[0][1:]}"
    airport_lat = airport_list[0].strip()
    airport_long = airport_list[1].strip()
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_lat}%2C{origin_long}&destinations={airport_lat}%2C{airport_long}&departure_time=now&key={maps_key}"

    response = requests.get(url, headers=headers, data=payload)
    readable_response = response.text
    response_list = readable_response.split(",")
    traffic_time = response_list[13].split(":")[-1].strip().strip("\"")

    return traffic_time



# normally the data would be inputted or generated elsewhere but this is a test so it's being generated here
today = date.today()
today_string = str(today)

year_slice = today_string[:4]
month_slice = today_string[5:7]
day_slice = today_string[8:]
flight_number = "6756"


origin, destination, time, startport_lat, startport_long, user_lat, user_long, traffic_time = get_flights_info(year_slice, month_slice, day_slice, flight_number)

print(f"origin: {origin}")
print(f"destination: {destination}")
print(f"departure time: {time}")
print(f"airport laongitude: {startport_long}")
print(f"airport latitude: {startport_lat}")
print(f"user longitude: {user_long}")
print(f"user latitude: {user_lat}")
print(f"travle time from current lcoation to airport: {traffic_time}")
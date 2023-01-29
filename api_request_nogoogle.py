import requests
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

            return origin_name, dest_name, time_formated, air_latitude, air_longitude
            # must return destination and originand departure time


# normally the data would be inputted or generated elsewhere but this is a test so it's being generated here
today = date.today()
today_string = str(today)

year_slice = today_string[:4]
month_slice = today_string[5:7]
day_slice = today_string[8:]
flight_number = "6756"


origin, destination, time, startport_lat, startport_long = get_flights_info(year_slice, month_slice, day_slice, flight_number)

print(f"origin: {origin}")
print(f"destination: {destination}")
print(f"departure time: {time}")
print(f"airport latitude: {startport_lat}")
print(f"airport longitude: {startport_long}")

from api_keys import *
import requests
from datetime import date
from datetime import datetime
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
            city_name = origin_list.split(":")[1][2:-1]

            destination = str(response["destination"])
            destination_list = destination.split(",")[1]
            dest_name = destination_list.split(":")[1][2:-1]

            timezone_list = origin.split(",")[2]
            timezone_name = timezone_list.split(":")[1][2:-1]

            leave_time = str(response["departureTime"])
            time_formated = datetime.strptime(leave_time, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo(timezone_name)).strftime('%I:%M %p')

            return city_name, dest_name, time_formated
            # must return destination and originand departure time
    
# normally the data would be inputted or generated elsewhere but this is a test so it's being generated here
today = date.today()
today_string = str(today)

year_slice = today_string[:4]
month_slice = today_string[5:7]
day_slice = today_string[8:]
flight_number = "5243"

# the api call method that gets the data
get_flights_info(year_slice, month_slice, day_slice, flight_number)
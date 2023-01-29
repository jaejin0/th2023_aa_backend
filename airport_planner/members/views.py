from django.template import loader
from django.http import HttpResponse
from .models import Member
import json
# Create your views here.

import requests
from datetime import date, datetime
from zoneinfo import ZoneInfo

def get_flights_info(year, month, day, flight_number):
    headers = {}
    payload = {}
    url = f"http://localhost:4000/flights?date={year}-{month}-{day}"
    response = requests.get(url, headers=headers, data=payload)
    readable_response = response.json()

    return readable_response

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def members(request, date, flightNumber):
    # normally the data would be inputted or generated elsewhere but this is a test so it's being generated here
    today_string = str(datetime.strptime(date, '%Y-%m-%d'))
    flightNumber = str(flightNumber).zfill(4)

    year_slice = today_string[:4]
    month_slice = today_string[5:7]
    day_slice = today_string[8:].split(' ')[0]

    readable_response = get_flights_info(year_slice, month_slice, day_slice, flightNumber)
    origin_name = ''
    dest_name = ''
    time_formated = ''

    for response in readable_response:
        if response["flightNumber"] == flightNumber:
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
    
    # template = loader.get_template('flights.html')
    context = {
        'departure' : origin_name,
        'arrival' : dest_name,
        'departureTime' : time_formated,
        'baggageTime' : 30, # placeholder values for calculations
        'tsaTime' : 25,
        'walkTime': 15
    }

    return HttpResponse(json.dumps(context))
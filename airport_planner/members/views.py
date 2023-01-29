from django.template import loader
from django.http import HttpResponse
from .models import Member
# Create your views here.

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def members(request, date, flightNumber):
    try:
        targetMember = Member.objects.get(flightNumber=flightNumber, date=date)
    except Member.DoesNotExist:
        targetMember = Member(flightNumber=flightNumber, date=date, checkInTime="900", tsa="1200", walkingTime="600")
        targetMember.save()    
    
    template = loader.get_template('flights.html')
    context = {
        'targetMember' : targetMember
    }
    return HttpResponse(template.render(context, request))

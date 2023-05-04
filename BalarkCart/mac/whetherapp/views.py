import json  
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required 
import urllib.request  
import json  
  
# Create your views here.  
@login_required(login_url= '/shop/login/') 
def whetherPage(request):  
    if request.method == 'POST':  
        # Get the city name from the user api = http://api.openweathermap.org/data/2.5/weather  
        city = request.POST.get('city', 'True')  
          
        # retreive the information using api  
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=imperial&appid=b3e2ecddca0f97a3abaee91b3b746684').read()  
          
        # convert json data file into python dictionary  
        list_of_data = json.loads(source)  
  
        # create dictionary and convert value in string  
        context = {  
            'city': city,  
            "country_code": str(list_of_data['sys']['country']),  
            "coordinate": str(list_of_data['coord']['lon']) + ' '  
                            + str(list_of_data['coord']['lat']),  
            "temp": str(round((list_of_data['main']['temp']-32)*(5/9)),2) + 'c',  
            "pressure": str(list_of_data['main']['pressure']),  
            "humidity": str(list_of_data['main']['humidity']),  
            "icon": str(list_of_data['weather'][0]['icon'])
        }  
    else:  
        context = {}  
      
    # send dictionary to the index.html  
    return render(request, 'whetherapp/index.html', context)  

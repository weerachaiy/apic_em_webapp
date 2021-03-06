from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .get_stuff import get_token, get_config, get_device_id, return_dict_example
from .bot import webhook_init, webhook


#Disable SSL warning
requests.packages.urllib3.disable_warnings()

# Create your views here.

apic_em_ip = "https://sandboxapic.cisco.com/api/v1"
catfacts_ip = 'http://catfacts-api.appspot.com/api'

def practice(request):
    requests.packages.urllib3.disable_warnings()
    api_call = "/facts"
    url = catfacts_ip + api_call
    header = '"text/html; charset=utf-8"'

    #get the cat fact - type will return as requests.models.Response
    my_response = requests.get(url, params='number=5', verify=False)

    #take the "utf-8" response value and convert it to a json disctionary
    data = json.loads(HttpResponse.getvalue(my_response).decode('utf-8'))

    #save one of the facts out to a variable
    response = data['facts'][0]

    return HttpResponse(response)

def index(request):
    template = loader.get_template('apic/index.html')
    auth_token = get_token(apic_em_ip)
    auth_token = json.loads(HttpResponse.getvalue(auth_token).decode('utf-8'))
    auth_token = auth_token['response']['serviceTicket']
    device_id = get_device_id(auth_token, apic_em_ip)
    config = get_config(auth_token, apic_em_ip, device_id)
    #output = config['response'].split('\n')
    context = {
        #'output': output,
        'ticket': auth_token,
        'deviceID': device_id,
    }

    return HttpResponse(template.render(context, request))

def apic_api(request):
    config = return_dict_example(apic_em_ip)

    return JsonResponse(config)

def wh_init(request):
    response = webhook_init()
    return HttpResponse(response)

@csrf_exempt
def sparkwebhook(request):
    wh_request = webhook(request)
    return HttpResponse('OK')

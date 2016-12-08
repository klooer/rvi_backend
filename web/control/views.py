import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from vehicles.models import Vehicle
import control.tasks


#@api_view(['POST'])
@csrf_exempt
def handle_control(request, vehicle_vin='-1'):

    print 'vehicle: ', vehicle_vin

    try:
        vehicle = Vehicle.objects.filter(veh_vin=vehicle_vin)[0]

        if request.method == 'POST':
            try:
                received_json_data = json.loads(request.body)
                print 'received json data', received_json_data
                command = received_json_data['command']
                print 'command: ', command
                try:
                    control.tasks.handle_control(vehicle, command)
                    response_data = str(received_json_data)
                    return HttpResponse(response_data, content_type="application/json")
                except Exception as e:
                    print str(e)
                    return HttpResponse('Send control command failed', content_type="plain/text")
            except:
                return HttpResponse('Invalid control message format', content_type="plain/text")
        else:
            return HttpResponse('POST action is expected', content_type="plain/text")
    except:
        return HttpResponse('No valid vehicle found.', content_type="plain/text")

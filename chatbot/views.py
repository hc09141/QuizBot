import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    print(request)
    print(request.GET)
    print(request.POST)
    if request.GET:
        return HttpResponse(request.GET['hub.challenge'])
    else:
        return HttpResponse()

# # Allows FB to validate our app
# def validate(request):
#     print('Get')
#     return HttpResponse(request.GET['hub.challenge'])

# # For receiving user messages
# def post(self, request, *args, **kwargs):
#     print('Post')
#     # Converts the text payload into a python dictionary
#     incoming_message = json.loads(self.request.body.decode('utf-8'))
#     # Facebook recommends going through every entry since they might send
#     # multiple messages in a single call during high load
#     for entry in incoming_message['entry']:
#         for message in entry['messaging']:
#             # Check to make sure the received call is a message call
#             # This might be delivery, optin, postback for other events 
#             if 'message' in message:
#                 print(message['message']['text'])
#                 process_message(entry['messaging']['sender']['id'], message['message']['text'])
#     return HttpResponse()

# def process_message(fb_id, msg):
#     # greeting = "Hi John! I'm alive!"
#     post_facebook_message(fb_id, msg)

# def post_facebook_message(fbid, message):         
#     post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' %(FACEBOOK_ACCESS_TOKEN) 
#     response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
#     status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
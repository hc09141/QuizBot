import json
import os
import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from OpenDBQuiz import OpenDBQuiz

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return validate(request)
    return process_messages(request)

# Allows FB to validate our app
def validate(request):
    print('Get')
    return HttpResponse(request.GET['hub.challenge'])

# For receiving user messages
def process_messages(request):
    print('Processing messages')
    # Converts the text payload into a python dictionary
    incoming_message = json.loads(request.body.decode('utf-8'))
    print(incoming_message)
    # Facebook recommends going through every entry since they might send
    # multiple messages in a single call during high load
    for entry in incoming_message['entry']:
        for message in entry['messaging']:
            # Check to make sure the received call is a message call
            # This might be delivery, optin, postback for other events 
            if 'message' in message:
                if 'text' in message['message']:
                    text = message['message']['text']
                    sender_id = message['sender']['id']
                    process_message(sender_id, text)
    return HttpResponse()

def process_message(fb_id, msg):
    # greeting = "Hi John! I'm alive!"
    post_facebook_message(fb_id, msg)

def post_facebook_message(fbid, message):         
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' %os.environ["PAGE_ACCESS_TOKEN"] 
    question = get_quiz_question()
    response_msg = json.dumps({
        "recipient":{"id":fbid}, 
        "message":{
            "text":question.question,
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":question.answer,
                    "payload":"<POSTBACK_PAYLOAD>",
                }
            ]
        }
    })

    quick_replies = response_msg["message"]["quick_replies"]
    wrong_answers = question.wrong_answers_set.all()
    for wrong_answer in wrong_answers:
        quick_replies.append({
            "content_type":"text",
            "title":wrong_answer.text,
            "payload":"<POSTBACK_PAYLOAD>",})

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def get_quiz_question():
    gQuiz = OpenDBQuiz()
    return gQuiz.get_questions(num_qs=1)[0]
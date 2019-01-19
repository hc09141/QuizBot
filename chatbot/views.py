from django.http import HttpResponse
from OpenDBQuiz import OpenDBQuiz, OpenDBCategories
# from rest_framework import viewsets
from .models import QuizQuestion
from django.views.decorators.csrf import csrf_exempt
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
    # return HttpResponse(request.GET['hub.challenge'])


@csrf_exempt
def create(request):
    result = json.loads(request.body)
    if 'set_id' in result:
        set_id = result['set_id']
    else:
        response = HttpResponse('Invalid JSON')
        response.status_code = 400
    for info in result['quiz_data']:
        quiz_question = info['question']
        quiz_answer = info['answer']
        quiz = QuizQuestion(question=quiz_question,
                            answer=quiz_answer,
                            set_id=set_id)
        quiz.save()
        print("Created: ", quiz)
    response = HttpResponse('Successfuly saved with set_id ' + set_id)
    response.status_code = 201
    return response

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
    print(question)
    response_msg = json.dumps({
        "recipient":{"id":fbid},
        "message":{
            "text":question['question'],
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":question["correct_answer"],
                    "payload":"<POSTBACK_PAYLOAD>",
                }
            ]
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def get_quiz_question():
    gQuiz = OpenDBQuiz()
    return gQuiz.get_questions(num_qs=1)

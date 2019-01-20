import json
import os
import random
import requests

from django.contrib.auth.models import User
from django.http import HttpResponse
from OpenDBQuiz import OpenDBQuiz, OpenDBCategories
# from rest_framework import viewsets
from .models import QuizQuestion, UserProfile, QuestionMessage, Message, QuestionResponseMessage
from django.views.decorators.csrf import csrf_exempt

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
                # if 'quick_reply' in message['message']:
                #     process_message(sender_id, message['message']['quick_reply']['text'])
            elif 'postback' in message:
                if 'title' in message['postback'] and message['postback']['title'] == 'Get Started':
                    sender_id = message['sender']['id']
                    process_new_user(sender_id)

    return HttpResponse()

def process_message(fb_id, msg):
    user_profile = UserProfile.objects.get(fb_id=fb_id)
    if user_profile.message_set:
        last_message = user_profile.message_set.last()
        if last_message.__class__.__name__ == 'QuestionMessage':
            post_trivia_answer(fb_id, msg, last_message)
            return
    post_trivia_question(fb_id)

def process_new_user(sender_id):
    user = User.objects.create_user('john', 'lennon@thebeatles.com')
    user_profile = UserProfile(fb_id=sender_id, user_id=user.id)
    user_profile.save()

def post_trivia_question(fbid):
    question = get_quiz_question()
    response_msg = {
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
    }

    wrong_answers = question.wrongoption_set.all()
    for wrong_answer in wrong_answers:
        print(wrong_answer)
        response_msg["message"]["quick_replies"].append({
            "content_type":"text",
            "title":wrong_answer.text,
            "payload":"<POSTBACK_PAYLOAD>",})

    random.shuffle(response_msg["message"]["quick_replies"])

    user_profile = UserProfile.objects.get(fb_id=fbid)
    message = QuestionMessage(question=question, user_profile=user_profile)
    message.save()

    post_facebook_message(fbid, response_msg)

def post_trivia_answer(fbid, user_answer, question_message):
    print("Post trivia answer")
    # saves user message (so that we register that they responded to prev question)
    message = QuestionResponseMessage(question_message=question_message, text=user_answer)
    message.save()

    response_msg = {
        "messaging_type": "<MESSAGING_TYPE>",
        "recipient": {"id": fbid},
        "message": {
            "text": "<RESPONSE GOING HERE>"
        }
    }
    correct_answer = question_message.question.correct_answer
    if correct_answer == user_answer:
        response_msg['message']['text'] = 'Correct!'
    else:
        response_msg['message']['text'] = 'Wrong! The correct answer was ' + correct_answer

    post_facebook_message(fbid, response_msg)


def post_facebook_message(fbid, response):
    print('Posting FB message')
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' %os.environ["PAGE_ACCESS_TOKEN"]

    response_msg = json.dumps(response)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def get_quiz_question():
    gQuiz = OpenDBQuiz()
    return gQuiz.get_questions(num_qs=1)[0]

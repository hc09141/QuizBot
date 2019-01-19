from django.http import HttpResponse
from OpenDBQuiz import OpenDBQuiz, OpenDBCategories
# from rest_framework import viewsets
from .models import QuizQuestion
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    gQuiz = OpenDBQuiz()
    print(gQuiz.get_questions(category=OpenDBCategories.entertaiment_comics))
    return HttpResponse('Hello!')
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

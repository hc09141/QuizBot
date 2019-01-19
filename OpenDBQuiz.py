import requests
import urllib
from chatbot.models import *
from enum import Enum


class OpenDBCategories(Enum):
    general_knowledge = 9
    entertainment_books = 10
    entertainment_film = 11
    entertainment_music = 12
    entertainment_musical = 13
    entertainment_television = 14
    entertainment_videogames = 15
    entertainment_boardgames = 16
    science_nature = 17
    science_computers = 18
    science_maths = 19
    mythology = 20
    sports = 21
    geography = 22
    history = 23
    politics = 24
    art = 25
    celebrities = 26
    animals = 27
    vehicles = 28
    entertaiment_comics = 29
    science_gadgets = 30
    entertainment_anime = 31
    entertainment_cartoons = 32


class OpenDBQuiz(object):

    def __init__(self):
        session_tokens_url = 'https://opentdb.com/api_token.php?command=request'
        authreq = requests.request('GET', session_tokens_url)
        token = authreq.json()['token']
        self.token = str(token)
        self.quiz_list = []
        # print(token)

    def get_questions(self, num_qs=10, category=None, difficulty=None):
        category_list = []
        category_list.append('amount=')
        category_list.append(str(num_qs))
        # Set category later, perhaps do as enum?
        if category is not None:
            category_list.extend(['&category=', str(category.value)])
        if difficulty is not None:
            category_list.extend(['&difficulty=', difficulty])
        category_list.extend(['&token=', self.token])
        category_list.append('&encode=url3986')
        url = 'https://opentdb.com/api.php?' + ''.join(category_list)
        qreq = requests.request('GET', url)
        # print(qreq)
        code = qreq.json()['response_code']
        # print(url)
        # print(code)
        quiz_object = self._quiz_question_objects(qreq.json())
        return quiz_object

    def _quiz_question_objects(self, json):
        quiz_list = []
        for element in json['results']:
            question = urllib.parse.unquote(element['question'])
            answer = urllib.parse.unquote(element['correct_answer'])
            question = QuizQuestion(question=question, answer=answer)
            question.save()
            for wrong_answer in element['incorrect_answers']:
                print(urllib.parse.unquote(wrong_answer))
                w = WrongOption(text=urllib.parse.unquote(wrong_answer), question=question)
                w.save()
            question.save()
            quiz_list.append(question)
        self.quiz_list.extend(quiz_list)
        return quiz_list

    # def __del__(self):
    #     for question in self.quiz_list:
    #         question.delete()


if __name__ == '__main__':
    gQuiz = OpenDBQuiz()
    # print(gQuiz.get_questions(category=OpenDBCategories.entertaiment_comics))

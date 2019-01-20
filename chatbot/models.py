from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# class strwImage(object):
#     def __init__(self, string, image_id=None):
#         # image_id is an optional string with the URL for the image
#         self.string = string
#         self.image_id = image_id

#     def __repr__(self):
#         repr_string = self.string
#         if self.image_id:
#             repr_string += 'image_id: '
#             repr_string += self.image_id
#         return repr_string


class QuizQuestion(models.Model):
    question = models.TextField()
    answer = models.TextField()
    set_id = models.CharField(max_length=100, default='')
    fb_id = models.CharField(max_length=50, default='0000')

    def __repr__(self):
        return "Q: " + str(self.question) + " A: " + str(self.answer) + " " + str(self.wrongoption_set.all())

    __str__ = __repr__


class WrongOption(models.Model):
    text = models.TextField()
    question = models.ForeignKey(QuizQuestion,
                                 on_delete=models.CASCADE)

    def __repr__(self):
        return str(self.text)

    __str__ = __repr__

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fb_id = models.CharField(unique=True, max_length=50)

class Message(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class QuestionMessage(Message):
    question = models.OneToOneField(QuizQuestion, on_delete=models.CASCADE, primary_key=True)

class QuestionResponseMessage(Message):
    text = models.TextField()
    question_message = models.OneToOneField(QuestionMessage, on_delete=models.CASCADE)

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


class WrongOption(models.Model):
    text = models.TextField()
    question = models.ForeignKey(QuizQuestion,
                                 on_delete=models.CASCADE)

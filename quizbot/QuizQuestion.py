class strwImage(object):
    def __init__(self, string, image_id=None):
        # image_id is an optional string with the URL for the image
        self.string = string
        self.image_id = image_id

    def __repr__(self):
        repr_string = self.string
        if self.image_id:
            repr_string += 'image_id: '
            repr_string += self.image_id
        return repr_string


class QuizQuestion(object):
    def __init__(self, question, answer, wrong_options=None):
        self.question = question
        self.answer = answer
        self.wrong_options = wrong_options

    def __repr__(self):
        return 'Question: ' + self.question.__repr__() + '\nAnswer: ' + self.answer.__repr__() + '\nWrong Answers: ' + self.wrong_options.__repr__() +'\n'

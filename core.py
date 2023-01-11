import pymorphy2

from loader import env

morph = pymorphy2.MorphAnalyzer()


class Test:
    def __init__(self, name, description, questions=None, results=None):
        self.name = name
        self.description = description
        self.questions = []
        self.results = []
        self.current_question = 0
        self.user_score = 0

        if questions is not None:
            self.questions = questions
        if results is not None:
            self.results = results

    @property
    def count_questions(self):
        return len(self.questions)

    def get_interpretation(self):
        interpretation = ''
        for score in self.results:
            if score.start <= self.user_score <= score.finish:
                interpretation = score.description
        return interpretation

    def get_question_text(self):
        text = f'Вопрос {str(self.current_question + 1)}: \n{self.questions[self.current_question].question}'
        return text.replace('\\n', '\n')

    def get_result_message(self):
        score = morph.parse('балл')[0].make_agree_with_number(self.user_score).word
        interpretation = self.get_interpretation()
        template = env.get_template('user_result_message.txt')
        text = template.render({'score': score, 'interpretation': interpretation, 'test': self})
        return text

    def get_message_to_admin(self, user):
        score = morph.parse('балл')[0].make_agree_with_number(self.user_score).word
        interpretation = self.get_interpretation()
        template = env.get_template('admin_result_message.txt')
        text = template.render({'user': user, 'score': score, 'interpretation': interpretation, 'test': self})
        return text

    def get_preview_message(self):
        title = '*' + self.name + '*'
        message = title + '\n' + self.description
        return message


class Question:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers


class Answer:
    def __init__(self, answer, point):
        self.answer = answer
        self.point = point


class Result:
    def __init__(self, start, finish, description):
        self.start = int(start)
        self.finish = int(finish)
        self.description = description.strip()

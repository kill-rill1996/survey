from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    """Опрос, который включает в себя один или несколько вопросов"""

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}. {self.title} - {self.start_date}'


class Question(models.Model):
    """Вопросы для опроса"""

    id = models.IntegerField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=512)
    is_text_question = models.BooleanField(default=False)
    only_one_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}. {self.survey.title} - {self.title}'


class Variant(models.Model):
    """Вариант ответа для вопроса"""

    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='variants')
    text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.id}. {self.question.title} - {self.text}'


class Answer(models.Model):
    """Объединяет все выбранные ответы пользователя на вопросы в одном опросе"""

    id = models.IntegerField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    answer_date = models.DateTimeField(auto_now_add=True)
    is_anon = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} ответ на опрос "{self.survey.title}"'


class Choice(models.Model):
    """Объект, показывающий выбор пользователя на один вопрос
    Если в вопросе нет вариантов ответа (т.е. вопрос текстовый), то
    сохраняем ответ пользователя в text_answer
    """

    id = models.IntegerField(primary_key=True)
    variant = models.ManyToManyField(Variant, blank=True, related_name='choices')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='choices')
    text_answer = models.TextField(blank=True)

    def __str__(self):
        if self.text_answer:
            return f'"{self.text_answer}" ответ на впрос из опроса "{self.answer.survey.title}"'
        return f'"{self.variant}" ответ на впрос из опроса "{self.answer.survey.title}'

    
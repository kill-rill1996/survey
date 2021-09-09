from rest_framework import serializers
from .models import Survey, Question, Variant, Choice, Answer
from django.contrib.auth.models import User


# Surveys list
class SurveyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        exclude = ('is_active',)


# Surveys detail
class VariantsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variant
        exclude = ('question',)


class QuestionsListSerializer(serializers.ModelSerializer):
    variants = VariantsListSerializer(many=True)

    class Meta:
        model = Question
        exclude = ('survey',)


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = QuestionsListSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'questions')


# Serializers for creating Surveys with Questions and Variants
class SurveyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        exclude = ('id', 'start_date')


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('id', )


class VariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        exclude = ('id',)


# Create Choice
class ChoiceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'


# Create Answer
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('id', 'survey')


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('id', 'answer_date')


# List похождение опросов всеми поьзователями
class VariantSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Variant
        fields = ('question', 'text')


class ChoiceSerializer(serializers.ModelSerializer):
    variant = VariantSerializer(many=True)

    class Meta:
        model = Choice
        exclude = ('id', 'answer')


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class AnswerListSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    user = UserNameSerializer()
    survey = serializers.CharField(source='survey.title')

    class Meta:
        model = Answer
        fields = ('user', 'is_anon', 'answer_date', 'survey', 'choices')



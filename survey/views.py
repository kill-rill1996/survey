from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .serializers import (SurveyListSerializer,
                          SurveyDetailSerializer,
                          SurveyCreateSerializer,
                          QuestionCreateSerializer,
                          VariantCreateSerializer,
                          ChoiceCreateSerializer,
                          CreateAnswerSerializer,
                          AnswerListSerializer,)

from .models import Survey, Answer, Variant, Question, Choice


class SurveyListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        survey = Survey.objects.filter(is_active=True)
        serializer = SurveyListSerializer(survey, many=True)
        return Response(serializer.data)


class SurveyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        survey = get_object_or_404(Survey, id=pk)
        serializer = SurveyDetailSerializer(survey)
        return Response(serializer.data)


class SurveyCreateView(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    serializer_class = SurveyCreateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Survey.objects.all()


class VariantViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    serializer_class = VariantCreateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Variant.objects.all()


class QuestionViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Question.objects.all()


class ChoiceViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceCreateSerializer

    def get_queryset(self):
        return Choice.objects.all()

    def create(self, request, *args, **kwargs):
        if (request.user == Answer.objects.filter(id=request.data['answer'])[0].user) or request.user.is_superuser:
            # if len(request.data['variant']) > 1:
            # print(request.data['variant'])
            #     if Variant.objects.filter(id=request.data['variant'])[0].question.only_one_answer:
            #         return Response(status=400)
            if (Variant.objects.filter(id=request.data['variant'])[0].question.is_text_question and request.data['text_answer'] == '' or (not Variant.objects.filter(id=request.data['variant'])[0].question.is_text_question and request.data['text_answer'] != '')):
                return Response(status=400)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=403)


class CreateAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data['is_anon'] == True:
            request.data['user'] = None
        answer = CreateAnswerSerializer(data=request.data)
        if answer.is_valid():
            answer.save()
        else:
            return Response(status=400)
        return Response(status=201)


class AnswerListViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = AnswerListSerializer

    def get_queryset(self):
        return Answer.objects.all().order_by('survey')


class UserAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.is_superuser or request.user.id == pk:
            answer = Answer.objects.filter(user__id=pk).order_by('answer_date')
            serializer = AnswerListSerializer(answer, many=True)
            return Response(serializer.data)
        return Response(status=403)

# class SurveyCreateView(APIView):
#     permission_classes = [IsAdminUser, ]
#
#     def post(self, request):
#         survey = SurveyCreateSerializer(data=request.data)
#         if survey.is_valid():
#             survey.save()
#         else:
#             return Response(status=400)
#         return Response(status=201)


# class QuestionCreateView(APIView):
#     permission_classes = [IsAdminUser, ]
#
#     def post(self, request):
#         question = QuestionCreateSerializer(data=request.data)
#         if question.is_valid():
#             question.save()
#         else:
#             return Response(status=400)
#         return Response(status=201)


# class VariantCreateView(APIView):
#     permission_classes = [IsAdminUser, ]
#
#     def post(self, request):
#         variant = VariantCreateSerializer(data=request.data)
#         if variant.is_valid():
#             variant.save()
#         else:
#             return Response(status=400)
#         return Response(status=201)

# class AnswersListView(APIView):
#     permission_classes = [IsAdminUser, ]
#
#     def get(self, request, pk):
#         answer = Answer.objects.filter(survey__id=pk)
#         serializer = AnswersListSerializer(answer, many=True)
#         return Response(serializer.data)
#
# class ChoiceCreateView(APIView):
#     permission_classes = [IsAdminUser, ]
#
#     def post(self, request):
#         choice = ChoiceCreateSerializer(data=request.data)
#         if choice.is_valid():
#             choice.save()
#         else:
#             return Response(status=400)
#         return Response(status=201)

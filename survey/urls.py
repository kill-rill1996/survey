from django.urls import path
from .views import (SurveyListView,
                    SurveyDetailView,
                    QuestionViewSet,
                    VariantViewSet,
                    SurveyCreateView,
                    ChoiceViewSet,
                    CreateAnswerView,
                    AnswerListViewSet,
                    UserAnswerView,
                    )


urlpatterns = [
    path('survey/', SurveyListView.as_view(), name='survey-list'),
    path('survey/<int:pk>/', SurveyDetailView.as_view(), name='survey-detail'),
    path("survey/create/", SurveyCreateView.as_view({'post': 'create'})),
    path("survey/create/<int:pk>/", SurveyCreateView.as_view({'post': 'update'})),
    path("survey/create/variant/", VariantViewSet.as_view({'post': 'create'})),
    path("survey/create/variant/<int:pk>/", VariantViewSet.as_view({'post': 'update'})),
    path("survey/create/question/", QuestionViewSet.as_view({'post': 'create'})),
    path("survey/create/question/<int:pk>/", QuestionViewSet.as_view({'post': 'update'})),
    path('survey/create/choice/', ChoiceViewSet.as_view({'post': 'create'})),
    path('survey/create/choice/<int:pk>/', ChoiceViewSet.as_view({'post': 'update'})),
    path('survey/create/answer/', CreateAnswerView.as_view()),
    path('survey/answers/', AnswerListViewSet.as_view({'get': 'list'})),
    path('survey/answers/<int:pk>/', UserAnswerView.as_view()),

    # path('survey/create/', SurveyCreateView.as_view()),
    # path('survey/create/question/', QuestionCreateView.as_view()),
    # path('survey/create/variant/', VariantCreateView.as_view()),
]
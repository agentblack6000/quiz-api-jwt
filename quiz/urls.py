from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from quiz import views

urlpatterns = [
    path("register/", views.StudentRegistrationView.as_view()),
    path("login/", obtain_auth_token),
    path("login", obtain_auth_token),
    path("questions/", views.QuestionList.as_view()),
    path("questions/<int:pk>/", views.DetailedQuestionView.as_view()),
    path("answers/", views.AddAnswerChoices.as_view()),
    path("student-list/", views.StudentClassList.as_view()),
    path("teacher-list/", views.TeacherList.as_view()),
    path("quiz-list/", views.QuizzesList.as_view()),
    path("quiz-list/<int:pk>/", views.DisplayQuiz.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

"""
views.py
"""
from django.db import models
from quiz.models import AnswerChoice, Question, Quizzes, Student, Teacher
from quiz.serializers import (
    AnswerChoiceSerializer,
    QuestionSerializer,
    QuizzesSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    TeacherSerializer,
    AttemptAnswerChoiceSerializer,
    AttemptQuestionSerializer,
    SubmitQuestionSerializer,
    SubmitAnswerChoiceSerializer,
    UserLoginTokenObtainPairSerializer,
)
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAdmin, IsTeacherOrAdmin


class StudentRegistrationView(generics.CreateAPIView):
    """
    Docstring for StudentRegistrationView
    """

    permission_classes = []
    serializer_class = StudentRegistrationSerializer


class UserLoginObtainTokenPairView(TokenObtainPairView):
    serializer_class = UserLoginTokenObtainPairSerializer


class QuestionList(generics.ListCreateAPIView):
    """
    Docstring for QuestionList
    """

    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class DetailedQuestionView(APIView):
    """
    Docstring for DetailedQuestionView
    """

    def get(self, request, pk, format=None):
        try:
            question = Question.objects.get(pk=pk)
            answer_choices = AnswerChoice.objects.filter(question=question)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        question_serializer = QuestionSerializer(question)
        answer_serializer = AnswerChoiceSerializer(answer_choices, many=True)

        return Response([question_serializer.data, answer_serializer.data])


class DisplayQuiz(APIView):
    """
    Docstring for DisplayQuiz
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            quiz = Quizzes.objects.get(pk=pk)
            questions = Question.objects.filter(associated_quizzes__id=pk)
            quiz_data = []

            for question in questions:
                answer_choices = AnswerChoice.objects.filter(question=question.id)
                question_data = AttemptQuestionSerializer(question).data
                answer_choices_data = AttemptAnswerChoiceSerializer(
                    answer_choices, many=True
                ).data
                quiz_data.append([question_data, answer_choices_data])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        quiz_serializer = QuizzesSerializer(quiz)
        return Response([quiz_serializer.data, quiz_data])


class AddAnswerChoices(generics.ListCreateAPIView):
    """
    Docstring for AddAnswerChoices
    """

    permission_classes = [IsTeacherOrAdmin]

    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer


class StudentClassList(generics.ListCreateAPIView):
    """
    Docstring for StudentClassList
    """

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class QuizzesList(generics.ListCreateAPIView):
    """
    Docstring for ViewQuizzes
    """

    permission_classes = [IsAuthenticated]

    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer


class TeacherList(generics.ListCreateAPIView):
    """
    Docstring for TeacherList
    """

    permission_classes = [IsAdmin]

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SubmitQuiz(APIView):
    """
    Docstring for SubmitQuiz
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk, format=None):
        try:
            quiz = Quizzes.objects.get(pk=pk)
            questions = Question.objects.filter(associated_quizzes__id=pk)
            quiz_data = []

            for question in questions:
                answer_choices = AnswerChoice.objects.filter(question=question.id)
                question_data = AttemptQuestionSerializer(question).data
                answer_choices_data = AttemptAnswerChoiceSerializer(
                    answer_choices, many=True
                ).data
                quiz_data.append([question_data, answer_choices_data])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        quiz_serializer = QuizzesSerializer(quiz)
        return Response([quiz_serializer.data, quiz_data])

    def post(self, request, pk, format=None):
        try:
            quizzes_serializer = QuizzesSerializer(data=request.data[0])
            
            if not quizzes_serializer.is_valid():
                print("quiz fail")
                raise Exception
            
            # TODO: Setup logic for prefetching related questions based on the Quiz ID instead
            # of performing multiple read operations on the DB

            quiz_attempt_data = request.data[1]

            score_calculation = []

            for question_answer_data in quiz_attempt_data:
                question_serializer = SubmitQuestionSerializer(
                    data=question_answer_data[0]
                )
                answer_choices_serializer = SubmitAnswerChoiceSerializer(
                    data=question_answer_data[1], many=True
                )

                if (
                    question_serializer.is_valid()
                    and answer_choices_serializer.is_valid()
                ):
                    question = Question.objects.get(id=question_serializer.data["id"])
                    answer_choices = AnswerChoice.objects.filter(is_correct=True, question=question)

                    correct_answer_ids = [choice.id for choice in answer_choices]

                    for choice in answer_choices_serializer.data:
                        if choice["is_correct"]:
                            if choice["id"] in correct_answer_ids:
                                score_calculation.append(question)
                else:
                    raise Exception

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        question_serializer = AttemptQuestionSerializer(score_calculation, many=True)
        return Response([question_serializer.data], status=status.HTTP_202_ACCEPTED)
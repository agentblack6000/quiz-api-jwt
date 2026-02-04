from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from quiz.models import AnswerChoice, Question, Quizzes
from quiz.serializers import AnswerChoiceSerializer, QuestionSerializer, QuizzesSerializer, StudentRegistrationSerializer
from .permissions import IsStudent, IsTeacher, IsTeacherOrAdmin

class StudentRegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = StudentRegistrationSerializer



class QuestionList(generics.ListCreateAPIView):
    """
    Docstring for QuestionList
    """
    permission_classes = [IsAuthenticated, ]
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        quiz_serializer = QuizzesSerializer(quiz)
        return Response(quiz_serializer.data)


class AddAnswerChoices(generics.ListCreateAPIView):
    """
    Docstring for AddAnswerChoices
    """
    permission_classes = [IsTeacherOrAdmin]

    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer


# class StudentClassList(generics.ListCreateAPIView):
#     """
#     Docstring for StudentClassList
#     """
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


class QuizzesList(generics.ListCreateAPIView):
    """
    Docstring for ViewQuizzes
    """
    permission_classes = [IsAuthenticated]

    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer


# class TeacherList(generics.ListCreateAPIView):
#     """
#     Docstring for TeacherList
#     """
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer

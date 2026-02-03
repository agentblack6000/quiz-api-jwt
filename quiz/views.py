from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from quiz.models import Question, AnswerChoice
from quiz.serializers import QuestionSerializer, AnswerChoiceSerializer


class QuestionList(APIView):
    """
    Docstring for QuestionList
    """

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




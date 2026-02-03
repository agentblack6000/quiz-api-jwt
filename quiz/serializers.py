from rest_framework import serializers
from quiz.models import Question, AnswerChoice

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text"]


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ["id", "choice_text", "question", "is_correct"]

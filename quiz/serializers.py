from django.contrib.auth.models import User, Group
from quiz.models import AnswerChoice, Question, Quizzes, Student, Teacher
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
        ]


class UserLoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "associated_quizzes"]


class QuizzesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = [
            "id",
            "title",
        ]


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ["id", "choice_text", "question", "is_correct"]


class AttemptQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text"]


class AttemptAnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ["id", "choice_text", "question"]


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        Student.objects.create(user=user)
        student_group = Group.objects.get(name="student")
        user.groups.add(student_group)

        return user


class StudentSerializer(UserSerializer):
    """
    Docstring for StudentSerializer
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


class TeacherSerializer(UserSerializer):
    """
    Docstring for TeacherSerializer
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "user"]

"""View module for handling requests about Questions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from appstationapp.models import Question

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for questions

    Arugments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Question
        # creates a clickable url for the API
        url = serializers.HyperlinkedIdentityField(
            view_name="question",
            lookup_field='id'
        )
        fields = ('id', 'is_from_interviewer', 'answer', 'user_id')


class Questions(ViewSet):
    """Questions for Application Station API"""

    # Handles POST
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Question instance
        """
        new_question = Question()
        new_question.question = request.data["question"]
        new_question.is_from_interviewer = request.data["is_from_interviewer"]
        # uncomment this line when AUTH is ready
        # new_question.user_id = request.auth.user.id
        # use this line UTNIL AUTH is ready
        new_question.user_id = request.data["user_id"]

        new_question.save()

        serializer = QuestionSerializer(
            new_question,
            context={'request': request}
        )

        return Response(serializer.data)

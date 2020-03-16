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
        fields = ('id', 'url', 'question', 'is_from_interviewer', 'answer', 'candidate_id')


class Questions(ViewSet):
    """Questions for Application Station API"""

    # Handles POST
    def create(self, request):
        """Handle POST for Question

        Fetch call to post question:
            http://localhost:8000/questions

        Returns:
            Response -- JSON serialized Question instance
        """
        new_question = Question.objects.create(
            question=request.data["question"],
            is_from_interviewer=request.data["is_from_interviewer"],
            candidate_id=request.auth.user.candidate.id
        )  

        serializer = QuestionSerializer(
            new_question,
            context={'request': request}
        )

        return Response(serializer.data)


    # Handles GET one ( example: questions/3 )
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single question

        Fetch call to get one question by question id:
            http://localhost:8000/questions/${id}

        Returns:
            Response -- JSON serialized Question instance
        """

        try:
            question = Question.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # filter by the logged in candidate
            if question.candidate.id == candidate_id:
                serializer = QuestionSerializer(question, context={'request': request})
                return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles GET all
    def list(self, request):
        """Handle GET requests to Questions

        Fetch call to get all questions:
            http://localhost:8000/questions

        Returns:
            Response -- JSON serialized list of questions
        """

        # list of question instances
        questions = Question.objects.all()

        # filter by the logged in candidate
        candidate_id = request.auth.user.candidate.id
        questions = questions.filter(candidate__id=candidate_id)

        # takes questions and converts to JSON
        serializer = QuestionSerializer(
            questions,
            many=True,
            context={'request': request}
        )

        # Return the JSON response
        return Response(serializer.data)

    
    # Handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for a question

        Fetch call to PUT one question by question id:
            http://localhost:8000/questions/${id}

        Fetch call to PUT answer to a question by question id:
            http://localhost:8000/questions/${id}?answer=true

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            question = Question.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # filter by the logged in candidate
            if question.candidate.id == candidate_id:

                # check to see if this is an update on an answer to a question
                is_answer = request.query_params.get('answer', False)

                if is_answer:
                    question.answer = request.data["answer"]
                else:
                    # need to update question, need to update is from interviewer
                    question.question = request.data["question"]
                    question.is_from_interviewer = request.data["is_from_interviewer"]

                question.save()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)
    

    # Handles DELETE
    def destroy(self, request, pk=None):
        """Handles DELETE requests for a single question

        Fetch call to DELETE one question by question id:
            http://localhost:8000/questions/${id}

        Returns:
            Response -- 204, 404, or 500 status code
        """
        try:
            question = Question.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # confirm logged in user owns the question being deleted
            if question.candidate.id == candidate_id:
                question.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Question.DoesNotExist as ex:
            return Response(
                {'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response({'message': ex.arg[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


"""View module for handling requests about statuses

    Users will NOT be able to create, update, or destroy a status. Users
    will retrieve and list statuses that are pre-populated in the database.
"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from appstationapp.models import Status


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for statuses

    Arugments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Status
        # creates a clickable url for the API
        url = serializers.HyperlinkedIdentityField(
            view_name="status",
            lookup_field='id'
        )
        fields = ('id', 'url', 'status')


class Statuses(ViewSet):
    """Statuses for Application Station"""

    # Handles GET one ( example: statuses/3 )
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single status

        Fetch call to get one status by status id:
            http://localhost:8000/statuses/${id}

        Returns:
            Response -- JSON serialized Status instance
        """

        try:
            status = Status.objects.get(pk=pk)
            serializer = StatusSerializer(status, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles GET all
    def list(self, request):
        """Handle GET requests to Statuses

        Fetch call to get all statuses:
            http://localhost:8000/statuses

        Returns:
            Response -- JSON serialized list of statuses
        """

        # list of status instances
        statuses = Status.objects.all()

        # takes statuses and converts to JSON
        serializer = StatusSerializer(
            statuses,
            many=True,
            context={'request': request}
        )

        # Return the JSON response
        return Response(serializer.data)


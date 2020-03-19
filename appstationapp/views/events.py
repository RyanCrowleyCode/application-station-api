"""View module for handling requests about Events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from appstationapp.models import Event, Job

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Events

    Arugments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Event
        # creates a clickable url for the API
        url = serializers.HyperlinkedIdentityField(
            view_name="event",
            lookup_field='id'
        )
        fields = ('id', 'url', 'details', 'start_time', 'end_time', 'job_id')


class Events(ViewSet):
    """Events for Application Station API"""

    # Handles POST
    def create(self, request):
        """Handle POST for Event

        Fetch call to post event:
            http://localhost:8000/events


        Returns:
            Response -- JSON serialized Question instance
        """

        try:
            # filter by the logged in customer for job, so that only the 
            # user who owns the job can create an event for the job
            candidate_id = request.auth.user.candidate.id
            job_candidate_id = Job.objects.get(pk=request.data["job_id"]).candidate.id

            if candidate_id == job_candidate_id:
                new_event = Event.objects.create(
                    details=request.data["details"],
                    start_time=request.data["start_time"],
                    end_time=request.data["end_time"],
                    job_id=request.data["job_id"]
                )  

                serializer = EventSerializer(
                    new_event,
                    context={'request': request}
                )

                return Response(serializer.data)
                
        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles GET one ( example: events/3 )
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single event

        Fetch call to get one event by event id:
            http://localhost:8000/events/${id}

        Returns:
            Response -- JSON serialized Event instance
        """

        try:
            event = Event.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # filter by the logged in candidate
            if event.job.candidate.id == candidate_id:
                serializer = EventSerializer(event, context={'request': request})
                return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles GET all
    def list(self, request):
        """Handle GET requests to Events

        Fetch call to get all events:
            http://localhost:8000/events

        Fetch call to get events based on job_id:
            http://localhost:8000/events?job_id=${job_id}

        Returns:
            Response -- JSON serialized list of events
        """

        # list of job instances
        events = Event.objects.all()

        # filter by the logged in candidate
        candidate_id = request.auth.user.candidate.id
        events = events.filter(job__candidate_id=candidate_id)

        # Get the job ID from the query params. If job_id filter events by job_id
        job_id = self.request.query_params.get('job_id', False)
        if job_id:
            events = events.filter(job__id=job_id)

        # takes events and converts to JSON
        serializer = EventSerializer(
            events,
            many=True,
            context={'request': request}
        )

        # Return the JSON response
        return Response(serializer.data)

    
    # Handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Fetch call to PUT one event by event id:
            http://localhost:8000/events/${id}

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # filter by the logged in candidate
            if event.job.candidate.id == candidate_id:

                # update event data
                event.details = request.data["details"]
                event.start_time = request.data["start_time"]
                event.end_time = request.data["end_time"]
                event.job_id = request.data["job_id"]

                event.save()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)
    

    # Handles DELETE
    def destroy(self, request, pk=None):
        """Handles DELETE requests for a single event

        Fetch call to DELETE one event by event id:
            http://localhost:8000/events/${id}

        Returns:
            Response -- 204, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # confirm that logged in user owns event being deleted
            if event.job.candidate.id == candidate_id:
                event.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response(
                {'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response({'message': ex.arg[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


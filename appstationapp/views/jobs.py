"""View module for handling requests about Jobs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from appstationapp.models import Job

class JobSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Jobs

    Arugments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Job
        # creates a clickable url for the API
        url = serializers.HyperlinkedIdentityField(
            view_name="job",
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'description', 'link', 'candidate_id', 'status_id', 'company_id')


class Jobs(ViewSet):
    """Jobs for Application Station API"""

    # Handles POST
    def create(self, request):
        """Handle POST for Job

        Fetch call to post job:
            http://localhost:8000/jobs

        Returns:
            Response -- JSON serialized Question instance
        """
        new_job = Job.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            link=request.data["link"],
            candidate_id=request.auth.user.candidate.id,
            status_id=request.data["status_id"],
            company_id=request.data["company_id"]
        )  

        serializer = JobSerializer(
            new_job,
            context={'request': request}
        )

        return Response(serializer.data)


    # Handles GET one ( example: jobs/3 )
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single job

        Fetch call to get one job by job id:
            http://localhost:8000/jobs/${id}

        Returns:
            Response -- JSON serialized Job instance
        """

        try:
            job = Job.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # filter by the logged in candidate
            if job.candidate.id == candidate_id:
                serializer = JobSerializer(job, context={'request': request})
                return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles GET all
    def list(self, request):
        """Handle GET requests to Jobs

        Fetch call to get all jobs:
            http://localhost:8000/jobs

        Returns:
            Response -- JSON serialized list of jobs
        """

        # list of job instances
        jobs = Job.objects.all()

        # filter by the logged in candidate
        candidate_id = request.auth.user.candidate.id
        jobs = jobs.filter(candidate__id=candidate_id)

        # takes jobs and converts to JSON
        serializer = JobSerializer(
            jobs,
            many=True,
            context={'request': request}
        )

        # Return the JSON response
        return Response(serializer.data)

    
    # Handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for a job

        Fetch call to PUT one job by job id:
            http://localhost:8000/jobs/${id}

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            job = Job.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # filter by the logged in candidate
            if job.candidate.id == candidate_id:

                # update job data
                job.title = request.data["title"]
                job.description = request.data["description"]
                job.link = request.data["link"]
                job.status_id = request.data["status_id"]
                job.company_id = request.data["company_id"]

                job.save()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)
    

    # Handles DELETE
    def destroy(self, request, pk=None):
        """Handles DELETE requests for a single job

        Fetch call to DELETE one job by job id:
            http://localhost:8000/jobs/${id}

        Returns:
            Response -- 204, 404, or 500 status code
        """
        try:
            job = Job.objects.get(pk=pk)
            candidate_id = request.auth.user.candidate.id

            # confirm that logged in user owns job being deleted
            if job.candidate.id == candidate_id:
                job.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Job.DoesNotExist as ex:
            return Response(
                {'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response({'message': ex.arg[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


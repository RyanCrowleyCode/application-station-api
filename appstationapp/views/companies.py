"""View module for handling requests about companies"""
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import serializers, status
from appstationapp.models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for companies

    Arugments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Company
        # creates a clickable url for the API
        url = serializers.HyperlinkedIdentityField(
            view_name="company",
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class Companies(ViewSet):
    """Companies for Application Station"""

    # Handles GET one ( example: questions/3 )
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single company

        Fetch call to get one company by company id:
            http://localhost:8000/companies/${id}

        Returns:
            Response -- JSON serialized Company instance
        """

        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles GET all
    def list(self, request):
        """Handle GET requests to Companies

        Fetch call to get all companies:
            http://localhost:8000/companies

        Returns:
            Response -- JSON serialized list of companies
        """

        # list of question instances
        companies = Company.objects.all()

        # takes questions and converts to JSON
        serializer = CompanySerializer(
            companies,
            many=True,
            context={'request': request}
        )

        # Return the JSON response
        return Response(serializer.data)


    # Handles POST
    def create(self, request):
        """Handle POST for Company

        Fetch call to post company:
            http://localhost:8000/companies

        Returns:
            Response -- JSON serialized Company instance
        """

        new_company = Company.objects.create(
            # all company names will be saved lowercase
            name=request.data["name"].lower(),
        )  

        serializer = CompanySerializer(
            new_company,
            context={'request': request}
        )

        return Response(serializer.data)


    # Handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for a company

        Fetch call to PUT one company by company id:
            http://localhost:8000/companies/${id}

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            company = Company.objects.get(pk=pk)
            company.name = request.data["name"]
            company.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handles DELETE
    def destroy(self, request, pk=None):
        """Handles DELETE requests for a single company

        Fetch call to DELETE one company by company id:
            http://localhost:8000/companies/${id}

        Returns:
            Response -- 204, 404, or 500 status code
        """

        try:
            company = Company.objects.get(pk=pk)
            company.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Company.DoesNotExist as ex:
            return Response(
                {'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return Response({'message': ex.arg[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
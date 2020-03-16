"""View module for handling requests about companies

    Users will NOT be able to delete or update a company. This is because 
    company names will NOT be user specific, and a user should not be able
    to update or delete a company that may be used by another user. The 
    effects of updating a company name will be to actually post a NEW
    company, and then update the company_id associated with that particular
    job.
"""
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

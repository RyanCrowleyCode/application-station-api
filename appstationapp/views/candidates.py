"""View module for handling requests about Candidates"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from appstationapp.models import Candidate


class CandidateSerializer(serializers.HyperlinkedIdentityField):
    """JSON serializer for Candidates

    Arugments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Candidate
        url = serializers.HyperlinkedIdentityField(
            view_name="candidates",
            lookup_field="id"
        )
        fields = ('id', 'user', 'address', 'city', 'phone', 'zipcode')
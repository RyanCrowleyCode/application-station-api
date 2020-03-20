"""View module for handling Login and Register"""
import json
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from appstationapp.models import Candidate


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Fetch call to login an existing user (POST)
        http://localhost:8000/login

    Arguments:
        Request -- the full HTTP request object
    '''

    # Load the JSON string of the request body into a dictionary
    req_body = json.loads(request.body.decode())

    # If the request is HTTP POST, try to pull out the relevent information
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided, so we can't log in the user
            data = json.dumps({'valid': False})
            return HttpResponse(data, content_type="application/json")


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication.

    Arguments:
        Request -- the full HTTP request object

    Fetch call to register a new user (POST)
        http://localhost:8000/register

    Returns:
        Token -- token in JSON
    '''

    # Load the JSON string of the request body into a dictionary
    req_body = json.loads(request.body.decode())

    try:
        # Create a new user by invoking the 'create_user' helper method
        # 'create_user' is built in to Django's User model
        new_user = User.objects.create_user(
            username=req_body['email'],
            email=req_body['email'],
            password=req_body['password'],
            first_name=req_body['first_name'],
            last_name=req_body['last_name'],
            is_active=True
        )

        # Now, create a Candidate where the user = new_user created above
        new_candidate = Candidate.objects.create(
            user=new_user
        )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)


        # Return the token to the client
        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')
    
    except Exception:
            data = json.dumps({'valid': False})
            return HttpResponse(data, content_type="application/json")



    
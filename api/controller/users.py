import json

from django.core import serializers

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def auth_login(username, password) :
    try :
        user = UserModel.objects.get(username=username)
    except UserModel.DoesNotExist :
        return 'Invalid username'

    if not user.check_password(password) :
        return 'Invalid password'

    # user_json = serializers.serialize('json', user)

    user_json = serializers.serialize('json', [user])  # Pass a list containing the user
    user_data = json.loads(user_json)[0]['fields']  # Convert JSON string to a dictionary and extract fields

    return 'Logged in successfully', user_data

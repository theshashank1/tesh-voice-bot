import json
import os

from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse


def index(request) :
    if request.method == 'GET' :
        user_cookie = request.COOKIES.get('user')

        if user_cookie :
            user = json.loads(user_cookie).get('username')
            return render(request, 'index.html', {'user' : user})

        return redirect(reverse('bot:login'))


def about(request) :
    file_path = os.path.join('requirements.txt')
    print(file_path)
    return FileResponse(open(file_path, 'rb'))


def login(request) :
    if request.method == 'GET' :
        return render(request, 'login.html')

import json

from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model


from .controller.bot import process_with_gemini

from .services import jwt_service, users


@csrf_exempt  # Disable CSRF (Cross-Site Request Forgery) protection for this view
def process(request) :
    if request.method == 'POST':
        try :
            # Assuming you're sending data as JSON in the request body
            data = json.loads(request.body)
            user_input = data.get('text', '')  # Adjust according to your JSON structure

            # parsed_output = process_handler(user_input)
            parsed_output = process_with_gemini(user_input)

            return JsonResponse({'response' : parsed_output})

        except json.JSONDecodeError :
            return JsonResponse({'error' : 'Invalid JSON format in request body'}, status=400)

        except Exception as e :
            return JsonResponse({'error' : str(e)}, status=500)

    return JsonResponse({'error' : 'Method not allowed'}, status=405)


def login(request) :
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        message, user_data = users.auth_login(username, password)

        if message == 'Logged in successfully':
            res = HttpResponseRedirect(reverse('bot:index'))


            res.set_cookie('user', jwt_service.encode_jwt(user_data))
            return res

            # return JsonResponse({'Message': message, 'User': user_data})

        return JsonResponse({'Message' : message}, status=401)

    return JsonResponse({'Message' : 'Method not allowed'}, status=405)


def register(request) :
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')

        UserModel = get_user_model()

        user = UserModel.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        return HttpResponseRedirect(reverse('bot:login'))




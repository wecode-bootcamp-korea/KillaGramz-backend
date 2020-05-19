import json
import bcrypt
import jwt

from django.views   import View
from django.http    import HttpResponse, JsonResponse

from .models    import Account

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "ALREADY EXIST"}, status=409)

            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode()
            Account.objects.create(
                    email       = data['email'],
                    password    = hashed_pw,
                    fullname    = data['fullname'],
                    username    = data['username'],

            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class SignInView(View):
    def post(self, request):
        account_data = json.loads(request.body)

        try:
            if Account.objects.filter(email=account_data['email']).exists() or Account.objects.filter(username=account_data['username']).exists() or Account.objects.filter(fullname=account_data['fullname']).exists():
                account = Account.objects.get(email=account_data['email'])

                encoded_pw = account.password.encode('utf-8')
                encoded_input = account_data['password'].encode('utf-8')
                if bcrypt.checkpw(encoded_input, encoded_pw):
                    token = jwt.encode({ 'email' : account.email }, 'secret', algorithm='HS256').decode('utf-8')
                    return JsonResponse({ 'access_token' : token }, status=200)
                return HttpResponse(status=403)

            return HttpResponse(status=402)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

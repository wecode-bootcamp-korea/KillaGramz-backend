import json
import bcrypt
import jwt

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.db.models       import Q
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from westagram.settings     import SECRET_KEY

from .models    import Account

class SignUpView(View):
    def post(self, request):
        
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email=data['email_or_phone']).exists():
                return JsonResponse({"message": "ALREADY EXIST"}, status=409)
            elif Account.objects.filter(username=data['username']).exists():
                return JsonResponse({"message": "ALREADY EXIST"}, status=409)

            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode()
            
            try:
                validate_email(data['email_or_phone'])
                Account.objects.create(
                        email       = data['email_or_phone'],
                        password    = hashed_pw,
                        fullname    = data['fullname'],
                        username    = data['username'],
                )
                
            except ValidationError:
                Account.objects.create(
                        password    = hashed_pw,
                        fullname    = data['fullname'],
                        username    = data['username'],
                        phone       = data['email_or_phone'],
                )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        if data['username_or_email_or_phone']:
            inserted_data = data['username_or_email_or_phone']
        
        try:
            if Account.objects.filter(Q(email=inserted_data) | Q(username=inserted_data) | Q(phone=inserted_data)).exists():
                
                account = Account.objects.get(Q(email=inserted_data) | Q(username=inserted_data) | Q(phone=inserted_data))

                encoded_pw = account.password.encode('utf-8')
                encoded_input = data['password'].encode('utf-8')
                
                if bcrypt.checkpw(encoded_input, encoded_pw):
                    token = jwt.encode({ 'username' : account.username }, SECRET_KEY, algorithm='HS256').decode('utf-8')
                    response = HttpResponse(status=200)
                    response['Authorization'] = token
                    
                    return JsonResponse({"access_token": token}, status=200)
                return HttpResponse(status=403)

            return JsonResponse({"message": "WRONG_INPUT"}, status=402)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
        


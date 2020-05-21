import json
import jwt

from django.views           import View
from django.http            import JsonResponse
from functools              import wraps
from django.db.models       import Q
from jwt                    import DecodeError

from .models                import Comment
from account.models         import Account
from westagram.settings     import SECRET_KEY

def login_required(func):
        #@wraps(func)
        def wrapper(self, request, *args, **kwargs):
            
            header_token    = request.META.get('HTTP_AUTHORIZATION', '')
            
            #header_token    = request.META['HTTP_AUTHORIZATION']
            #given_token     = json.loads(request.body)['access_token']
            decoded_token   = jwt.decode(header_token,SECRET_KEY, algorithm='HS256')['username']
            
            try:
                if Account.objects.filter(username=decoded_token).exists():
                    return func(self, request, *args, **kwargs)
                else:
                    return JsonResponse({"message": "username does not exist"})
            except jwt.DecodeError:
                return JsonResponse({"message": "WRONG_TOKEN!"}, status=403)
            except KeyError:
                return JsonResponse({"message": "Key Error"}, status=405)
            except Account.objects.filter(username=decoded_token).DoesNotExist:
                return JsonResponse({"message": "User Not Found"}, status=406)
        return wrapper


class CommentView(View):

    @login_required
    def post(self, request):
        
        header_token    = request.META.get('HTTP_AUTHORIZATION', '')
        #header_token    = request.META['HTTP_AUTHORIZATION']
        data            = json.loads(request.body)
        #given_token     = json.loads(request.body)['access_token']
        decoded_token   = jwt.decode(header_token,SECRET_KEY, algorithm='HS256')['username']
        account         = Account.objects.get(username=decoded_token)

        Comment.objects.create(
                account     = account,
                content     = data['content'],
                username    = decoded_token
        )
        all_comments = list(Comment.objects.all().values('username', 'content'))

        return JsonResponse({"message":all_comments}, status=200)

    def get(self, request):
        return JsonResponse({'comment':list(Comment.objects.all().values('username', 'content'))}, status=200)



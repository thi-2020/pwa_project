from accounts.models import User

class EmailBackend(object):
    def authenticate(self, request, email=None, password=None, **kwargs):
        
        try:
            user = User.objects.get(email=email)
            print("user in @8s",user)
        except Exception as e:
            print("error in @10 in modelbackend is",e)
            return None
        else:
            return user
            # if getattr(user, 'is_active', False) and  user.check_password(password):
            #     return user
        return None


    def get_user(self, user_id):
        User = get_user_model()        
        try:
            return User.objects.get(id=user_id)
        except Exception as e:
            print("error in @21 in modelbackend is",e)
            return None
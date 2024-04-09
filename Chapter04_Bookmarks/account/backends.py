from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class EmailAuthBackend:
    print("Authenticate using Email")
    
    def authenticate(self, request, username = None, password = None):
        try:
            print(username)
            user = UserModel.objects.get(email__iexact = username)
            print("User", user)
            print(password)
            if user.check_password(password):
                return user
            return None
        except(UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk = user_id)
        except UserModel.DoesNotExist:
            return None

from django.contrib.auth.models import User

#The preceding code is a simple authentication backend.
class EmailAuthBackend(object):
    '''Authenticate using an e-mail address'''
    def authenticate(self, request, username=None, password=None):
# The authenticate() method receives a request object and the username and
# password optional parameters
        try:
            # retireve user with email and check password wch handles the password hashing to compare the given
# password against the password stored in the database
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None

        except User.DoesNotExist:
            return None
    # get the user through ID set
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


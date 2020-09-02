from django.db import models
from django.conf import settings

class Profile(models.Model):
    '''The user one-to-one field allows you to associate profiles with
users.'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    data_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                               blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    objects = models.Manager()

#################NB#################################
'''In order to keep your code generic, use the get_user_model() method to retrieve
the user model and the AUTH_USER_MODEL setting to refer to it when defining a
model's relations to the user model, instead of referring to the auth user
model directly.'''
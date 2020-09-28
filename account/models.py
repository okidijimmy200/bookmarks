from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    '''The user one-to-one field allows you to associate profiles with
users.'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
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



# Let's create an intermediary model to build relationships between users
class Contact(models.Model):
    # User_from: A ForeignKey for the user who creates the relationship
    user_form = models.ForeignKey('auth.User', related_name='rel_from_set',
                                 on_delete=models.CASCADE)
# user_to: A ForeignKey for the user being followed
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set',
                                on_delete=models.CASCADE)
# created: A DateTimeField field with auto_now_add=True to store the time
# when the relationship was created
    created = models.DateTimeField(auto_now_add=True,
                                    db_index=True)
# A database index is automatically created on the ForeignKey fields. You use db_
# index=True to create a database index for the created field. This will improve
# query performance when ordering QuerySets by this field
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

#  Add following field to User dynamically
user_model = get_user_model() #retreive user model provided by django
'''In order to access the end side of the relationship from the User
model, it would be desirable for User to contain a ManyToManyField'''
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact,
                        related_name='followers',
                        symmetrical=False)) #we use add_to_class() to avoid adding custom user model, not recommended for other scenarios

'''tell Django to use your custom intermediary model
for the relationship by adding through=Contact to the ManyToManyField. This
is a many-to-many relationship from the User model to itself'''
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# shows the Action model that will be used to store user activities.
class Action(models.Model):
# user: The user who performed the action; this is a ForeignKey to the Django User model.
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
# verb: The verb describing the action that the user has performed.
    verb = models.CharField(max_length=255)
# This will tell you the model for the relationship and points to the ContentType model
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
#PositiveIntegerField to match Django's automatic primary key fields ie stroing the primary key
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
# A field to define and manage the generic relation using the two previous fields
    target = GenericForeignKey('target_ct', 'target_id')
# created: The date and time when this action was created. You use auto_ now_add=True to automatically set this to the current datetime when the
# object is saved for the first time in the database.
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)
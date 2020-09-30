import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

# The create_action() function allows you to create actions that optionally include
# a target object. this can be used in your code as a shortcut to
# add new actions to the activity stream.
def create_action(user, verb, target=None):
     # check for any similar action made in the last minute
# Sometimes, your users might click several times on the LIKE or UNLIKE button or perform the same action multiple times in a short period of time. This will easily
# lead to storing and displaying duplicate actions
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                       verb= verb,
                                       created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
                                             target_ct=target_ct,
                                             target_id=target.id) 

    if not similar_actions:
    # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False

'''
to avoid duplicate actions
1)First, you get the current time using the timezone.now() method provided
by Django.
2)You use the last_minute variable to store the datetime from one minute
ago and retrieve any identical actions performed by the user since then.
3)You create an Action object if no identical action already exists in the last
minute. You return True if an Action object was created, or False otherwise.
'''
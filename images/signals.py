# attach a receiver function to the m2m_changed signal.
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

'''register the users_like_changed function as a receiver function using the
receiver(), attach it to the m2m_changed signal'''
# -------------------------------------------------------------
'''connect
the function to Image.users_like.through so that the function is only called if the
m2m_changed signal has been launched by this sender'''
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()

'''You have to connect your receiver function to a signal so that it gets called every
time the signal is sent and we register them by importing the ready method'''
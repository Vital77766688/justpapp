
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *


# @receiver(post_save, sender=Chat)
# def create_contact(sender, instance, created, **kwargs):
# 	if created and instance.is_group_chat:
# 		group_chat = GroupChat.objects.create(creator=,)
# 		group_chat.admins.add()
# 	else:
# 		instance.contact.save()
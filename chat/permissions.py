from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from .models import *


def get_key(kwargs:dict) -> str:
	key = None
	for k in ['chat__id', 'chat_chat__id']:
		key = kwargs.get(k)
		if key:
			break
	return key



class IsChatUser(BasePermission):
	def has_permission(self, request, view):
		key = get_key(view.kwargs)
		if not key:
			return True
		try:
			return request.user.chats.get(chat__id=key)
		except ObjectDoesNotExist:
			return False


class IsChatAdminOrOwner(BasePermission):
	def has_permission(self, request, view):
		try:
			chat = request.user.chats.get(chat__id=get_key(view.kwargs))
			return chat.is_admin or chat.is_owner
		except ObjectDoesNotExist:
			return False
			

class IsChatOwner(BasePermission):
	def has_permission(self, request, view):
		try:
			return request.user.chats.get(chat__id=get_key(view.kwargs)).is_owner
		except ObjectDoesNotExist:
			return False


class IsMessageAuthor(BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.message.author == request.user
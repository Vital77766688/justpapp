from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import *


class ReadWriteMessagePermission(BasePermission):
	def has_permission(self, request, view):
		chat = get_object_or_404(Chat, pk=view.kwargs['chat_pk'])
		return chat.users.filter(pk=request.user.pk).exists()


class DeleteMessagePermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		if view.action == 'complete_delete':
			if obj.message.author == request.user:
				return True
			else:
				return obj.chat.group.admins.filter(pk=request.user.pk).exists()
		return True


class UpdateMessagePermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		if view.action in ('update', 'partial_update'):
			return obj.message.author == request.user
		return True


class UpdateChatPermission(BasePermission):
	def has_object_permission(self, request, view, obj):
		if obj.is_group_chat:
			if obj.creator == request.user:
				return True
			elif view.action in ('update', 'partial_update'):
				return obj.group.admins.filter(pk=request.user.pk).exists()
			elif view.action == 'add_remove_admin':
				return request.user.username == request.data['admin'] and request.data['remove_admin'] == 'true'
		return True

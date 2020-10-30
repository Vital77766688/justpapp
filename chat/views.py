from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import *
from .serializers import *
from .models import *


class ChatViewSet(ModelViewSet):
	serializer_class = ChatListSerializer
	permission_classes = (permissions.IsAuthenticated,
						  UpdateChatPermission)

	def get_serializer_class(self):
		print(self.action)
		if self.action == 'create':
			return PrivateChatCreateSerializer
		elif self.action == 'create_group':
			return GroupChatCreateSerializer
		elif self.action in ('update', 'partial_update'):
			return GroupChatUpdateSerializer
		elif self.action == 'add_remove_admin':
			return GroupChatUpdateAdminSerializer
		return self.serializer_class
	
	def get_queryset(self):
		return self.request.user.chats.all()


	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.is_group_chat:
			return super().update(request, args, kwargs)
		return Response('You cannot update a private chat', status=status.HTTP_400_BAD_REQUEST)


	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.is_group_chat:
			if instance.users.all().count() > 1:
				if instance.group.admins.all().count() > 1:
					instance.group.admins.remove(request.user)
				else:
					if instance.group.admins.filter(id=request.user.id):
						return Response('You cannot leave the group. You are the only admin in this group.', status=status.HTTP_400_BAD_REQUEST)
				instance.users.remove(request.user)
			else:
				self.perform_destroy(instance)
		else:
			if instance.users.all().count() > 1:
				instance.users.remove(request.user)
			else:
				self.perform_destroy(instance)
		return Response(status=status.HTTP_204_NO_CONTENT)


	@action(['post'], detail=False)
	def create_group(self, request, *args, **kwargs):
		return self.create(request)

	@action(['put', 'patch'], detail=True)
	def add_remove_admin(self, request, *args, **kwargs):
		return self.update(request)



class MessageViewSet(ModelViewSet):
	lookup_field = 'message__id'
	serializer_class = UserMessageListSerializer
	permission_classes = (permissions.IsAuthenticated,
						  ReadWriteMessagePermission,
						  DeleteMessagePermission,
						  UpdateMessagePermission,)

	def get_serializer_class(self):
		if self.action in ('create', 'update', 'partial_update'):
			return UserMessageCreateUpdateSerializer
		return self.serializer_class

	def get_queryset(self):
		return UserMessage.objects.filter(user=self.request.user, chat=self.kwargs['chat_pk'])


	@action(['delete'], detail=True)
	def complete_delete(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.message.author == request.user:
			self.perform_destroy(instance.message)
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response('You cannot delete this message', status=status.HTTP_400_BAD_REQUEST)
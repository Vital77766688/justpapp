from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import *
from .serializers import *
from .models import *

User = get_user_model()


class UserViewSet(ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	http_method_names = ('get', 'options')


class ContactViewSet(ModelViewSet):
	serializer_class = ContactListRetrieveSerializer

	def get_queryset(self):
		return self.request.user.contacts.all()

	def get_serializer_class(self):
		if self.action == 'create':
			return ContactCreateSerializer
		elif self.action == 'send_message':
			return ContactMessageSerializer
		return self.serializer_class

	@action(['post'], detail=True)
	def send_message(self, request, *args, **kwargs):
		return self.create(request)


class ChatViewSet(ModelViewSet):
	lookup_field = 'chat__id'
	lookup_url_kwarg = 'chat__id'
	serializer_class = ChatListRetrieveDestroySerializer

	def get_queryset(self):
		if self.action in ('update', 'partial_update', 'set_owner'):
			self.lookup_field = 'pk'
			return Chat.objects.filter(users__user=self.request.user)
		return self.request.user.chats.all()

	def get_serializer_class(self):
		if self.action == 'create':
			return GroupChatCreateSerializer
		elif self.action in ('update', 'partial_update', 'set_owner'):
			return GroupChatUpdateSerializer
		elif self.action == 'add_admin':
			return ChatAddAdminSerializer
		elif self.action == 'remove_admin':
			return ChatRemoveAdminSerializer
		elif self.action == 'add_users':
			return ChatAddUsersSerializer
		elif self.action == 'remove_user':
			return ChatRemoveUserSerializer
		return self.serializer_class

	def get_permissions(self):
		permissions = self.permission_classes
		if self.action in ('update', 'partial_update', 'add_users', 'remove_users'):
			self.permission_classes = permissions + [IsChatAdminOrOwner,]
		elif self.action in ('set_owner', 'add_admin', 'remove_admin'):
			self.permission_classes = permissions + [IsChatOwner,]
		else:
			self.permission_classes = permissions + [IsChatUser,]
		return super().get_permissions()

	def update(self, request, *args, **kwargs):
		if request.data.get('owner') and self.action != 'set_owner':
			request.data.pop('owner')
		self.kwargs['partial'] = True
		return super().update(request, args, kwargs)

	def destroy(self, request, *args, **kwargs):
		chat = self.get_object()
		if chat.is_owner:
			return Response("You cannot leave the chat unless you are the owner", status=status.HTTP_400_BAD_REQUEST)
		return super().destroy(request, args, kwargs)

	@action(['post'], detail=True)
	def set_owner(self, request, *args, **kwargs):
		owner = request.data.get('owner')
		if owner:
			request.data.clear()
			request.data['owner'] = owner
			return self.update(request, args, kwargs)
		return Response("You should provide owner in request's body", status=status.HTTP_400_BAD_REQUEST)

	@action(['post'], detail=True)
	def add_users(self, request, *args, **kwargs):
		self.kwargs['chat'] = self.get_object().chat
		return self.create(request, args, kwargs)

	@action(['post'], detail=True)
	def remove_user(self, request, *args, **kwargs):
		self.kwargs['chat'] = self.get_object().chat
		return self.create(request, args, kwargs)

	@action(['post'], detail=True)
	def add_admin(self, request, *args, **kwargs):
		self.kwargs['chat'] = self.get_object().chat
		return self.create(request, args, kwargs)

	@action(['post'], detail=True)
	def remove_admin(self, request, *args, **kwargs):
		self.kwargs['chat'] = self.get_object().chat
		return self.create(request, args, kwargs)


class MessageViewSet(ModelViewSet):
	lookup_field = 'message__id'
	serializer_class = MessageSerializer

	def get_queryset(self):
		return self.request.user.messages.filter(chat__id=self.kwargs['chat_chat__id'])

	def get_permissions(self):
		permissions = self.permission_classes
		if self.action in ('update', 'partial_update', 'delete_from_all'):
			self.permission_classes = permissions + [IsMessageAuthor,]
		return super().get_permissions()

	@action(['delete'], detail=True)
	def delete_from_all(self, request, *args, **kwargs):
		instance = self.get_object()
		self.perform_destroy(instance.message)
		return Response(status=status.HTTP_204_NO_CONTENT)

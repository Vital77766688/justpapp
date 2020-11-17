from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .exceptions import *
from .models import *


User = get_user_model()


class ChatMixin:
	def get_instance(self, instance):
		return (
			instance.chat,
			instance,
		)

	def is_group_chat(self, instance):
		if instance.is_group_chat:
			return True
		raise serializers.ValidationError('You cannot manage private chats')

	def to_representation(self, instance):
		chat, instance = self.get_instance(instance)
		last_message = instance.last_message
		unread_messages = chat.messages. \
							filter(user=instance.user, read_date__isnull=True). \
							exclude(message__author=instance.user). \
							count()
		result = {
			'id': chat.id,
			'last_message': last_message.text[:20] if last_message else None,
			'last_message_date': last_message.create_date if last_message else None,
			'unread_messages': unread_messages,
			'is_group_chat': chat.is_group_chat,
		}
		if chat.is_group_chat:
			users = [(u.user.username, u.is_admin) for u in chat.users.all()]
			result['chat_name'] = chat.chat_name
			result['creator'] = chat.creator.username
			result['owner'] = chat.users.get(is_owner=True).user.username
			result['users'] = [user[0] for user in users]
			result['admins'] = [user[0] for user in users if user[1]]
		else:
			result['user'] = instance.chat_contact.username

		return result


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username']


class ContactListRetrieveSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	contact = serializers.ReadOnlyField(source='contact.username')

	class Meta:
		model = Contact
		fields = ['id', 'user', 'contact', 'contact_display_name']


class ContactCreateSerializer(serializers.Serializer):
	contact = serializers.CharField()
	contact_display_name = serializers.CharField(max_length=50, required=False)

	def validate_contact(self, value):
		try:
			return User.objects.get(username=value)
		except ObjectDoesNotExist:
			raise serializers.ValidationError('No such user')

	def create(self, validated_data, *args, **kwargs):
		user = self.context['request'].user
		contact = user.contacts.get_or_create(contact=validated_data.get('contact'), \
											  contact_display_name=validated_data.get('contact_display_name'))
		return contact[0]


class ContactMessageSerializer(serializers.Serializer):
	message = serializers.CharField()

	def validate(self, attrs):
		# TODO validate contact id
		return attrs

	def create(self, validated_data, *args, **kwargs):
		author = self.context['request'].user
		contact_id = self.context['view'].kwargs.get('pk')
		with transaction.atomic():
			message = Message.objects.create(author=author, text=validated_data['message'])
			author.contacts.get(pk=contact_id).send_message(message)
		return message

	def to_representation(self, instance):
		return {
			'id': instance.id,
			'create_date': instance.create_date,
			'author': instance.author.username,
			'text': instance.text
		}


class ChatListRetrieveDestroySerializer(ChatMixin, serializers.ModelSerializer):
	class Meta:
		model = UserChat


class GroupChatCreateSerializer(ChatMixin, serializers.Serializer):
	users = serializers.ListField(child=serializers.CharField())
	chat_name = serializers.CharField(max_length=50)

	def create(self, validated_data):
		creator = self.context['request'].user
		users = User.objects.filter(username__in=validated_data['users'])
		chat = Chat.objects.create_group(chat_name=validated_data['chat_name'], \
										 creator=creator, \
										 users=users)
		return chat.users.get(user=creator)


class GroupChatUpdateSerializer(ChatMixin, serializers.ModelSerializer):
	chat_name = serializers.CharField(required=False)
	owner = serializers.CharField(required=False, write_only=True)

	class Meta:
		model = Chat
		fields = ['chat_name', 'owner']

	def validate_owner(self, value):
		try:
			return User.objects.get(username=value)
		except ObjectDoesNotExist:
			raise serializers.ValidationError('User does not exists')

	def update(self, instance, validated_data):
		self.is_group_chat(instance)
		if validated_data.get('owner'):
			instance.set_owner(validated_data['owner'])
		return super().update(instance, validated_data)

	def get_instance(self, instance):
		return (
			instance,
			instance.users.get(user__id=self.context['request'].user.id)
		)


class ChatManageSerializer(ChatMixin, serializers.Serializer):
	def get_chat(self):
		chat = self.context['view'].kwargs.get('chat')
		if not chat:
			raise serializers.ValidationError('No chat instance')
		_ = self.is_group_chat(chat)
		return chat

	def to_representation(self, instance):
		return instance


class ChatAddAdminSerializer(ChatManageSerializer):
	admin = serializers.CharField()

	def validate_admin(self, value):
		chat = self.get_chat()
		try:
			return chat.users.get(user__username=value, is_admin=False).user
		except ObjectDoesNotExist:
			raise serializers.ValidationError('User does not exists or is not a chat member or user is already admin')

	def create(self, validated_data, *args, **kwargs):
		chat = self.get_chat()
		chat.add_admin(validated_data['admin'])
		return {'detail': f"{validated_data['admin'].username} has been added to admins"}


class ChatRemoveAdminSerializer(ChatManageSerializer):
	admin = serializers.CharField()

	def validate_admin(self, value):
		chat = self.get_chat()
		try:
			admin = chat.users.get(user__username=value, is_admin=True).user
			return admin
		except ObjectDoesNotExist:
			raise serializers.ValidationError('User does not exists or is not a chat member or user is not admin')

	def create(self, validated_data, *args, **kwargs):
		chat = self.get_chat()
		chat.remove_admin(validated_data['admin'])
		return {'detail': f"{validated_data['admin'].username} has been removed from admins"}


class ChatAddUsersSerializer(ChatManageSerializer):
	users = serializers.ListField(child=serializers.CharField())

	def validate(self, attrs):
		chat = self.get_chat()
		users = User.objects. \
					filter(username__in=attrs['users']). \
					exclude(id__in=[u.user.id for u in chat.users.all()])
		return {
			'add_users': users,
			'skip_users': [username for username in attrs['users'] if not username in [u.username for u in users]]
		}


	def create(self, validated_data, *args, **kwargs):
		chat = self.get_chat()
		with transaction.atomic():
			for user in validated_data['add_users']:
				chat.add_user(user)
		return {
			'users_added': [u.username for u in validated_data['add_users']],
			'users_skipped': validated_data['skip_users'],
		}


class ChatRemoveUserSerializer(ChatManageSerializer):
	user = serializers.CharField()

	def validate_user(self, value):
		chat = self.get_chat()
		try:
			return chat.users.get(user__username=value).user
		except ObjectDoesNotExist:
			raise serializers.ValidationError('User does not exists or user is not member of the chat')

	def create(self, validated_data, *args, **kwargs):
		chat = self.get_chat()
		chat.remove_user(validated_data['user'])
		return {'detail': f"{validated_data['user'].username} was successfuly removed from the chat"}


class MessageSerializer(serializers.ModelSerializer):
	message = serializers.CharField()

	class Meta:
		model = UserMessage
		fields = ('message',)

	def create(self, validated_data):
		author = self.context['request'].user
		chat_id = self.context['view'].kwargs.get('chat_chat__id')
		with transaction.atomic():
			message = Message.objects.create(author=author, text=validated_data['message'])
			try:
				author.chats.get(chat__id=chat_id).send_message(message)
			except ObjectDoesNotExist:
				raise serializers.ValidationError('Chat does not exists')
		return author.messages.get(chat__id=chat_id, message=message)

	def update(self, instance, validated_data):
		instance.message.text = validated_data['message']
		instance.message.save()
		return instance

	def to_representation(self, instance):
		return {
			'id': instance.message.id,
			'author': instance.message.author.username,
			'create_date': instance.message.create_date,
			'text': instance.message.text,
		}

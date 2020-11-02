from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .exceptions import *
from .models import *


User = get_user_model()


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
		except User.DoesNotExist:
			raise serializers.ValidationError('No such user')

	def create(self, validated_data, *args, **kwargs):
		user = self.context['request'].user
		contact = user.contacts.get_or_create(contact=validated_data.get('contact'), \
											  contact_display_name=validated_data.get('contact_display_name'))
		return contact[0]


class ContactMessageSerializer(serializers.Serializer):
	message = serializers.CharField()

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


class ChatListRetrieveDestroySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserChat

	def to_representation(self, instance):
		last_message = instance.chat.messages.all().order_by('-id')[0].message \
					   if instance.chat.messages.exists() else None

		if instance.chat.is_group_chat:
			return {
				'id': instance.chat.id,
				'chat_name': instance.chat.group.chat_name,
				'creator': instance.chat.group.creator.username,
				'owner': instance.chat.group.owner.username,
				'users': [user.user.username for user in instance.chat.users.all()],
				'admins': [admin.username for admin in instance.chat.group.admins.all()],
				'last_message': last_message.text[:20] if last_message else None,
				'last_message_date': last_message.create_date if last_message else None,
				'unread_messages': instance.chat.messages \
									.filter(user=instance.user, read_date__isnull=True) \
									.exclude(message__author=instance.user) \
									.count(),
				'is_group_chat': instance.chat.is_group_chat,
			}
		else:
			return {
				'id': instance.chat.id,
				'user': instance.chat_contact.username,
				'last_message': last_message.text[:20] if last_message else None,
				'last_message_date': last_message.create_date if last_message else None,
				'unread_messages': instance.chat.messages \
									.filter(user=instance.user, read_date__isnull=True) \
									.exclude(message__author=instance.user) \
									.count(),
				'is_group_chat': instance.chat.is_group_chat,
			}


class GroupChatCreateSerializer(serializers.Serializer):
	users = serializers.ListField(child=serializers.CharField())
	chat_name = serializers.CharField(max_length=50)

	def create(self, validated_data):
		creator = self.context['request'].user
		users = User.objects.filter(username__in=validated_data['users'])
		chat = Chat.objects.create_group(chat_name=validated_data['chat_name'], \
										 creator=creator, \
										 users=users)
		return chat.users.get(user=creator)

	def to_representation(self, instance):
		return ChatListRetrieveDestroySerializer(instance).data


class GroupChatUpdateSerializer(serializers.ModelSerializer):
	chat_name = serializers.CharField(required=False)
	owner = serializers.SlugRelatedField(many=False, \
										 read_only=False, \
										 queryset=User.objects.all(), \
										 slug_field='username')

	class Meta:
		model = GroupChat
		fields = ['chat_name', 'owner']

	def update(self, instance, validated_data):
		print(validated_data, instance)
		return super().update(instance, validated_data)

	def to_representation(self, instance):
		user_chat_instance = instance.chat.users.get(user=self.context['request'].user)
		return ChatListRetrieveDestroySerializer(user_chat_instance).data


class ChatManageAdminSerializer(serializers.Serializer):
	admin = serializers.CharField()

	def validate_admin(self, value):
		try:
			return User.objects.get(username=value)
		except User.DoesNotExist:
			raise serializers.ValidationError('No such user')

	def create(self, validated_data, *args, **kwargs):
		chat = GroupChat.objects.get(chat__id=self.context['view'].kwargs.get('chat__id'))
		if self.context['view'].action == 'add_admin':
			try:
				chat.add_admin(validated_data['admin'])
			except UserIsNotInChat:
				raise serializers.ValidationError('User should be a member of this group')
		elif self.context['view'].action == 'remove_admin':
			chat.remove_admin(validated_data['admin'])

		return chat

	def to_representation(self, instance):
		user_chat_instance = instance.chat.users.get(user=self.context['request'].user)
		return ChatListRetrieveDestroySerializer(user_chat_instance).data


class ChatManageUsersSerializer(serializers.Serializer):
	users = serializers.ListField(child=serializers.CharField())

	def validate_users(self, value):
		return User.objects.filter(username__in=value)

	def create(self, validated_data, *args, **kwargs):
		chat = GroupChat.objects.get(chat__id=self.context['view'].kwargs.get('chat__id'))
		if self.context['view'].action == 'add_users':
			chat.add_users(validated_data['users'])
		elif self.context['view'].action == 'remove_users':
			chat.remove_users(validated_data['users'])

		return chat

	def to_representation(self, instance):
		user_chat_instance = instance.chat.users.get(user=self.context['request'].user)
		return ChatListRetrieveDestroySerializer(user_chat_instance).data


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserMessage




































# class GetUsersMixin:
# 	def get_users(self, users):
# 		return User.objects.filter(username__in=users)


# class ChatListSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Chat

# 	def to_representation(self, instance):
# 		user = self.context['request'].user
# 		last_message = instance.messages.all().order_by('-id')[0].message \
# 					   if instance.messages.exists() else None

# 		if instance.is_group_chat:
# 			return {
# 				'id': instance.id,
# 				'chat_name': instance.group.chat_name,
# 				'creator': instance.creator.username,
# 				'users': [user.username for user in instance.users.all()],
# 				'admins': [user.username for user in instance.group.admins.all()],
# 				'create_date': instance.create_date,
# 				'last_message': last_message.text[:20] if last_message else None,
# 				'last_message_date': last_message.create_date if last_message else None,
# 				'unread_messages': instance.messages \
# 									.filter(user=user, read_date__isnull=True) \
# 									.exclude(message__author=user) \
# 									.count(),
# 				'is_group_chat': instance.is_group_chat,
# 			}
# 		else:
# 			return {
# 				'id': instance.id,
# 				'user': instance.users.exclude(id=user.id).first().username,
# 				'create_date': instance.create_date,
# 				'last_message': last_message.text[:20] if last_message else None,
# 				'last_message_date': last_message.create_date if last_message else None,
# 				'unread_messages': instance.messages \
# 									.filter(user=user, read_date__isnull=True) \
# 									.exclude(message__author=user) \
# 									.count(),
# 				'is_group_chat': instance.is_group_chat,
# 			}


# class PrivateChatCreateSerializer(serializers.Serializer):
# 	user = serializers.CharField()

# 	def create(self, validated_data, *args, **kwargs):
# 		creator = self.context['request'].user
# 		user = User.objects.get(username=validated_data['user'])
# 		chat = Chat.objects.create(is_group_chat=False, creator=creator)
# 		chat.users.add(*[creator, user])
# 		return chat

# 	def validate(self, attrs):
# 		try:
# 			user = User.objects.get(username=attrs.get('user'))
# 		except User.DoesNotExist:
# 			raise serializers.ValidationError('User with such username does not exist')
# 		return attrs


# 	def to_representation(self, instance):
# 		return {
# 			'id': instance.id,
# 			'users': [user.username for user in instance.users.all()]
# 		}


# class GroupChatCreateSerializer(GetUsersMixin, serializers.Serializer):
# 	users = serializers.ListField(child=serializers.CharField())
# 	chat_name = serializers.CharField(max_length=50)

# 	def create(self, validated_data):
# 		creator = self.context['request'].user
# 		users = self.get_users(validated_data.get('users'))
# 		users |= User.objects.filter(pk=creator.pk)
# 		chat = Chat.objects.create(is_group_chat=True, creator=creator)
# 		chat.users.add(*users)
# 		group = GroupChat.objects.create(chat=chat, chat_name=validated_data['chat_name'])
# 		return chat

# 	def to_representation(self, instance):
# 		return {
# 			'id': instance.id,
# 			'chat_name': instance.group.chat_name,
# 			'users': [user.username for user in instance.users.all()]
# 		}


# class GroupChatUpdateAbstractSerializer(GetUsersMixin, serializers.Serializer):
# 	def perform_update(self, instance):
# 		instance.save()
# 		instance.group.save()
# 		return instance

# 	def to_representation(self, instance):
# 		return {
# 			'id': instance.id,
# 			'chat_name': instance.group.chat_name,
# 			'creator': instance.creator.username,
# 			'users': [user.username for user in instance.users.all()],
# 			'admins': [user.username for user in instance.group.admins.all()],
# 			'create_date': instance.create_date,
# 			'is_group_chat': instance.is_group_chat,
# 		}


# class GroupChatUpdateSerializer(GroupChatUpdateAbstractSerializer):
# 	chat_name = serializers.CharField(max_length=50, required=False)
# 	add_users = serializers.ListField(child=serializers.CharField(), required=False)
# 	remove_users = serializers.ListField(child=serializers.CharField(), required=False)

# 	def update(self, instance, validated_data):
# 		new_chat_name = validated_data.get('chat_name')
# 		if new_chat_name:
# 			instance.group.chat_name = new_chat_name
		
# 		add_users = validated_data.get('add_users')
# 		if add_users:
# 			instance.users.add(*self.get_users(add_users))
		
# 		remove_users = validated_data.get('remove_users')
# 		if remove_users:
# 			instance.users.remove(*self.get_users(remove_users))

# 		return self.perform_update(instance)


# class GroupChatUpdateAdminSerializer(GroupChatUpdateAbstractSerializer):
# 	admin = serializers.CharField()
# 	remove_admin = serializers.BooleanField()

# 	def update(self, instance, validated_data):
# 		if validated_data.get('remove_admin'):
# 			try:
# 				admin = instance.group.admins.get(username=validated_data.get('admin'))
# 				instance.group.admins.remove(admin)
# 			except User.DoesNotExist:
# 				raise serializers.ValidationError('Cannot be done. User is not admin')
# 		else:
# 			try:
# 				admin = instance.users.get(username=validated_data.get('admin'))
# 				instance.group.admins.add(admin)
# 			except User.DoesNotExist:
# 				raise serializers.ValidationError('User should be a chat participant')

# 		return self.perform_update(instance)




# class UserMessageListSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = UserMessage

# 	def to_representation(self, instance):
# 		return {
# 			'id': instance.message.id,
# 			'text': instance.message.text,
# 			'author': instance.message.author.username,
# 			'create_date': instance.message.create_date,
# 			'delivery_date': instance.delivery_date,
# 			'read_date': instance.read_date,
# 		}


# class UserMessageCreateUpdateSerializer(serializers.Serializer):
# 	text = serializers.CharField()

# 	def create(self, validated_data):
# 		author = self.context['request'].user
# 		try:
# 			chat = Chat.objects.get(pk=self.context['view'].kwargs['chat_pk'])
# 		except Chat.DoesNotExist:
# 			raise serializers.ValidationError('There is no chat with provided ID')
# 		message = Message.objects.create(author=author, text=validated_data['text'])
# 		for user in chat.users.all():
# 			chat.messages.create(chat=chat, user=user, message=message)
# 		return message

# 	def update(self, instance, validated_data):
# 		instance.message.text = validated_data['text']
# 		instance.message.save()
# 		return instance.message

# 	def to_representation(self, instance):
# 		return {
# 			'id': instance.id,
# 			'text': instance.text,
# 			'author': instance.author.username,
# 			'create_date': instance.create_date,
# 		}
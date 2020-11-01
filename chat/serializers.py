from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


User = get_user_model()


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
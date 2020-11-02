from django.db import transaction
from django.db import models
from django.contrib.auth import get_user_model
from .exceptions import *

User = get_user_model()


class ChatManager(models.Manager):
	def create(self, contact):
		with transaction.atomic():
			chat = super().create()
			chat.add_users_from_contact(contact)
		return chat

	def create_group(self, chat_name, creator, users=[]):
		with transaction.atomic():
			chat = super().create(is_group_chat=True)
			group = GroupChat(chat_name=chat_name, creator=creator, owner=creator)
			chat.group = group
			group.save()
			chat.save()
			users_set = set(users)
			users_set.add(creator)
			for user in users_set:
				chat.add_user(user=user)
		return chat


class Chat(models.Model):
	is_group_chat = models.BooleanField(default=False)
	group = models.OneToOneField('GroupChat', on_delete=models.CASCADE, related_name='chat', null=True)

	objects = ChatManager()

	def send_message(self, message):
		if not self.users.filter(user=message.author).exists():
			raise UserIsNotInChat
		with transaction.atomic():
			for user in self.users.all():
				self.messages.create(user=user.user, message=message)

	def add_user(self, user, chat_contact=None):
		if not self.users.filter(user=user).exists():
			self.users.create(user=user, chat_contact=chat_contact)

	def add_users_from_contact(self, contact):
		self.add_user(contact.user, contact.contact)
		self.add_user(contact.contact, contact.user)


class GroupChat(models.Model):
	chat_name = models.CharField(max_length=50)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_groups')
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
	admins = models.ManyToManyField(User)

	def add_admin(self, user):
		if self.chat.users.filter(user=user).exists():
			self.admins.add(user)
		else:
			raise UserIsNotInChat

	def remove_admin(self, user):
		self.admins.remove(user)

	def add_users(self, users):
		with transaction.atomic():
			for user in users:
				self.chat.add_user(user=user)

	def remove_users(self, users):
		with transaction.atomic():
			self.admins.remove(*users)
			self.chat.users.filter(user__in=users).delete()


class UserChat(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='users')
	chat_contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

	def __str__(self):
		f = self.user.username
		t = self.chat_contact.username if not self.chat.is_group_chat else self.chat.group.chat_name
		return f"{f}: {t}"
	
	def delete(self):
		self.chat.messages.filter(user=self.user).delete()
		return super().delete()

	def send_message(self, message):
		if not self.chat.is_group_chat:
			self.chat.add_user(user=self.chat_contact, chat_contact=self.user)
		self.chat.send_message(message=message)

	class Meta:
		unique_together = ['user', 'chat']


class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
	contact = models.ForeignKey(User, on_delete=models.CASCADE)
	contact_display_name = models.CharField(max_length=50, null=True)

	def __str__(self):
		return f"{self.user.username} - {self.contact.username}"

	def _get_user_chat(self):
		return self.user.chats.get(chat_contact=self.contact)

	def _get_contact_chat(self):
		chat = self.contact.chats.get(chat_contact=self.user).chat
		return self.user.chats.create(chat=chat, chat_contact=self.contact)

	def _create_chat(self):
		Chat.objects.create(self)
		return self._get_user_chat()

	def _get_chat(self):
		handlers = [self._get_user_chat, self._get_contact_chat, self._create_chat]
		for handler in handlers:
			try:
				return handler()
			except Exception as e:
				continue
		raise CannotGetChat

	def send_message(self, message):
		self._get_chat().send_message(message)

	class Meta:
		unique_together = ['user', 'contact']


class Message(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	create_date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	def __str__(self):
		return f"{self.text[:20]} by {self.author.username}"


class UserMessage(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	delivery_date = models.DateTimeField(blank=True, null=True)
	read_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return f"{self.user.username}: {self.message.text[:20]} by {self.message.author.username}"

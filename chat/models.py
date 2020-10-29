from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
	users = models.ManyToManyField(User, related_name='chats')
	create_date = models.DateTimeField(auto_now_add=True)
	is_group_chat = models.BooleanField(default=False)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_created_chats')

	def __str__(self):
		return f"{', '.join([user.username for user in self.users.all()[:5]])}..."


class GroupChat(models.Model):
	chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='group')
	chat_name = models.CharField(max_length=50, blank=True, null=True)
	admins = models.ManyToManyField(User, related_name='my_admin_chats')

	def __str__(self):
		return self.chat_name if self.chat_name else chat


class Message(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	create_date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	def __str__(self):
		return f"{self.create_date}: {self.author.username}: {self.text[:20]}"


class UserMessage(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	delivery_date = models.DateTimeField(blank=True, null=True)
	read_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.message.__str__()

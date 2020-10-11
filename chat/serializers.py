from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UsersListSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields= ['id', 'username', 'email', 'first_name', 'last_name']
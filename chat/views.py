from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UsersListSerializer

UserModel = get_user_model()


class UsersListView(generics.ListAPIView):
	serializer_class = UsersListSerializer

	def get_object(self):
		return self.request.user

	def get_queryset(self):
		user = self.request.user
		return UserModel.objects.exclude(pk=self.get_object().pk)
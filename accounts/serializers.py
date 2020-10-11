from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from allauth.account.models import EmailAddress
from dj_rest_auth.models import TokenModel
from django.contrib.auth.models import User

UserModel = get_user_model()

class PasswordResetSerializer(PasswordResetSerializer):
	def get_email_options(self): 
		return {
			'subject_template_name': settings.PASSWORD_RESET_SUBJECT_TEMPLATE,
			'email_template_name': settings.PASSWORD_RESET_EMAIL_TEMPLATE,
		}


class UserDetailsSerializer(serializers.ModelSerializer):
	verified = serializers.SerializerMethodField()

	class Meta:
		model = UserModel
		fields = ('username', 'email', 'verified', 'first_name', 'last_name', 'is_staff')

	def get_verified(self, obj):
		try:
			return EmailAddress.objects.get_primary(obj).verified 
		except AttributeError:
			return None

	def validate_email(self, email):
		request = self.context['request']
		email = get_adapter().clean_email(email)
		if allauth_settings.UNIQUE_EMAIL:
			if email and email_address_exists(email, request.user):
				raise serializers.ValidationError(
					_("A user is already registered with this e-mail address."))
		return email


	def update(self, instance, validated_data):
		request = self.context.get('request')
		email = validated_data.get('email')
		if email and email != instance.email:
			email_address = EmailAddress.objects.get_primary(instance)
			if email_address:
				email_address.change(request, email, confirm=True)
		return super().update(instance, validated_data)


class TokenSerializer(serializers.ModelSerializer):
	user = UserDetailsSerializer()

	class Meta:
		model = TokenModel
		fields = ('key', 'user',)
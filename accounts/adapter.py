from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
	def get_from_email(self):
		current_site = get_current_site(self.request)
		return f'noreply@{current_site.domain}'

	def send_confirmation_mail(self, request, emailconfirmation, signup):
		current_site = get_current_site(request)
		
		ctx = {
			"user": emailconfirmation.email_address.user,
			"protocol": 'https' if request.is_secure() else 'http',
			"site_name": current_site.name,
			"domain": current_site.domain,
			"key": emailconfirmation.key,
		}
		if signup:
			email_template = settings.EMAIL_CONFIRMATION_SIGNUP
		else:
			email_template = settings.EMAIL_CONFIRMATION
		self.send_mail(email_template,
						emailconfirmation.email_address.email,
						ctx)

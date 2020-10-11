from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from allauth.account.utils import send_email_confirmation


class ResendConfirmationEmailView(GenericAPIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		send_email_confirmation(request, request.user)
		return Response(
            {"detail": "Confirm e-mail link has been sent."},
            status=status.HTTP_200_OK
        )
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import ResendConfirmationEmailView

urlpatterns = [
	# path('', include('chat.urls')),
	path('auth/resend-confirmation-email/', ResendConfirmationEmailView.as_view(), name='resend_confirmation_email'),
	path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
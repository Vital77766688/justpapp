from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from accounts.views import ResendConfirmationEmailView

urlpatterns = [
	path('api/chat/', include('chat.urls')),
	path('auth/resend-confirmation-email/', ResendConfirmationEmailView.as_view(), name='resend_confirmation_email'),
	path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
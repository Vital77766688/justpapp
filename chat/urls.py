from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import *

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('contacts', ContactViewSet, basename='contacts')
router.register('chats', ChatViewSet, basename='chats')

# message_router = NestedSimpleRouter(router, 'chats', lookup='chat')
# message_router.register('messages', MessageViewSet, basename='messages')


urlpatterns = [
	path('', include(router.urls)),
	# path('', include(message_router.urls)),
]

from django.urls import path, include
from rest_framework_nested import routers
from .views import *


router = routers.SimpleRouter
router.register('contacts', ContactViewSet)
router.register('chats', ChatViewSet)

chat_router = routers.NestedSimpleRouter(router, 'chats', lookup='chat')
chat_router.register('messages', MessageViewSet, basename='messages')


urlpatterns = [
	path('', include(router.urls)),
	path('', include(chat_router.urls)),
]

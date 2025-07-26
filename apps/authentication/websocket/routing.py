from django.urls import re_path
from apps.authentication.websocket import consumer

websocket_urlpatterns = [
    re_path(r"ws/somepath/$", consumer.SendFromServerConsumer.as_asgi()),
]
from django.urls import path, include
from .views import CustomizeRestCaptchaView

app_name = 'captcha_app'

urlpatterns = [
    path('captcha/', CustomizeRestCaptchaView.as_view(), name='captcha')
]

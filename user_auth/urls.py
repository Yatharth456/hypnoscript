from django.urls import path
from .views import Register, UserVerification, LoginUser




urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('verify/', UserVerification.as_view(), name='verify'),
    path('login/', LoginUser.as_view(), name='login'),
]
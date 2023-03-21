from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer
from .models import User
from django.conf import settings
from django.core.mail import send_mail
from config import Config
from django.contrib.auth.hashers import make_password
from random_word import RandomWords
from django.template.loader import render_to_string
# from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
import base64, ast

# Create your views here.
class Register(APIView):
    def post(self, request):
        data = request.data
        r = RandomWords()
        password = r.get_random_word()
        print(password,"password")
        email = data['email']

        hashed_password = make_password(password, salt=Config.SALT)
        username = r.get_random_word()
        data['username'] = username
        data['password'] = hashed_password
        cred = {'username':username, 'password':password, 'email':email}
        encode = str(cred).encode('UTF-8')
        encoded = base64.b64encode(encode)
        print(str(encoded, 'UTF-8'),"encoded_data")
        subject = 'welcome to my site.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        context = {'email':email, 'verification_link':f'http://65.108.77.50:8000/auth/verify/?data={str(encoded, "UTF-8")}' ,'username':username, 'password':password}
        
        html_content = render_to_string(
        'auth/email.html', context=context
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body="This is body",
            from_email=email_from,
            to=recipient_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        message = f'Click here for verify'
        return Response ({"msg": "User register temporarily. Please check your email and click on link for verification."})

class UserVerification(APIView):
    def get(self, request):
        params = request.GET.get('data')
        decrypted_data = base64.b64decode(params).decode('UTF-8')
        dict_data = ast.literal_eval(decrypted_data)
        data = request.data
        data['email'] = dict_data['email']
        data['username'] = dict_data['username']
        data['password'] = dict_data['password']
        serializer = RegisterUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg": "User data saved in database."})
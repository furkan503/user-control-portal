# from users.api.serializers import UserSerializer
# from users.models import Todo, Post, Album, Comment, Photo



# import os
# import django
# import requests


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()


# from django.contrib.auth.models import User



# users_response = requests.get('https://jsonplaceholder.typicode.com/users')
# users_data = users_response.json()


# for user_data in users_data:
#     user = User.objects.create(
#         name=user_data['name'],
#         email=user_data['email'],
#         website=user_data['website'],
#         phone=user_data['phone'],
#         street=user_data['address.street'],
#         suite=user_data['address.suite'],
#         city=user_data['address.city'],
#         company=user_data['company.name']


#     )
#     print(user_data)
#     user.save()

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     gender = models.CharField(max_length=50)
#     is_login = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.user.username} Profile'


class Chat(models.Model):
    content = models.CharField(max_length=1222)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

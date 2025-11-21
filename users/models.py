from django.db import models

class User(models.Model):
    id_users = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.TextField(max_length=254, null=True, default='temp')

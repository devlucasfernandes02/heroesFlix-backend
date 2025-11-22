from django.db import models

class User(models.Model):
    id_users = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.TextField(max_length=254, null=True, default='temp')

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    
    avatar_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"
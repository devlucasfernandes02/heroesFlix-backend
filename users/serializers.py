from rest_framework import serializers
from .models import Profile, User
from django.contrib.auth.password_validation import validate_password
import random

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','password','password2')
        read_only_fields = ('id',)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"password": "As senhas não conferem."})
        # validações extras de senha do Django
        validate_password(data.get('password'))
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'name', 'avatar_url')
        read_only_fields = ('id', 'avatar_url',)
        
    # Limita a 5 perfis)
    def validate(self, data):
        user = data.get('user')
        
        
        if Profile.objects.filter(user=user).count() >= 5:
            raise serializers.ValidationError({"limite": "Você já atingiu o limite de 5 perfis para esta conta."})
            
        return data

    # (Gera a string do ícone)
    def create(self, validated_data):
        
        profile_name = validated_data.get('name', 'P') 
        initial = profile_name[0].upper() 
        random_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        
        validated_data['avatar_url'] = initial + random_letter 
        
       
        return super().create(validated_data)
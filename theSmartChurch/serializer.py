from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import Profile,Project, Announcements,Wedding

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=('bio','email','profile_picture','user','contact')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=('image','title','description','link','user')
class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Announcements
        fields=('title','description','user')

class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wedding

        fields=('groomName','bridename','phone','date','status','comment')

    def validate(self, data):
         
           phone= data.get('phone')

           if  phone:
               raise serializers.ValidationError("phone already registered")

           return data     

       
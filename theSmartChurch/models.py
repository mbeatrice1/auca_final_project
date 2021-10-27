from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models import Q
from django.db import models
from django.db.models.fields import DateField
from embed_video.fields import EmbedVideoField

class Item(models.Model):
    video = EmbedVideoField()
class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email


# Create your models here.

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture =models.ImageField(upload_to= 'profiles/', blank=True, default='profiles/default.png')
    bio = models.CharField(max_length=500, default='No bio')
    email=models.EmailField(max_length=200,null=True)
    contact = models.CharField(max_length=80)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_bio(cls,id, bio):
        update_profile = cls.objects.filter(id = id).update(bio = bio)
        return update_profile

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile
    @classmethod
    def search_user(cls,user):
        return cls.objects.filter(user__username__icontains=user).all()

class Project(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default='')
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=250)
    country = models.CharField(max_length=50)

    

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Project.objects.filter(Q(title__icontains=searchterm)|Q(description__icontains=searchterm)|Q(country__icontains=searchterm))
        return search
        
class Announcements(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Announcements.objects.filter(Q(title__icontains=searchterm)|Q(description__icontains=searchterm)|Q(country__icontains=searchterm))
        return search


class JoinService(models.Model):
    firstname = models.CharField(max_length =30,null=True)
    lastname = models.CharField(max_length =30,null=True)
    phoneNmber=models.CharField(max_length=20,null=True)
    add=models.CharField(max_length =30,null=True)
    email = models.EmailField(null=True)
    dateRe = models.TextField(null=True)

    def __str__(self):
        return self.firstname
    class Meta:
        ordering = ['firstname']

    def save_joinService(self):
       self.save()

    def delete_joinService(self):
        self.delete()

    
class  Congregants(models.Model):
    firstname = models.CharField(max_length =30,null=True)
    lastname = models.CharField(max_length =30,null=True)
    phoneNumber=models.CharField(max_length=20,null=True)
    address=models.CharField(max_length =30,null=True)
    DOB=models.DateField(null=True)
    email = models.EmailField(null=True)
    gender=models.CharField(max_length=30,null=True)
    maritalStatus=models.CharField(max_length=30,null=True)
    date=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.firstname
    class Meta:
        ordering = ['firstname']

    def save_congregant(self):
        self.save()

    def delete_congregant(self):
        self.delete()

    def update_congregant(self):
        self.update_congregant()    


    
class Department(models.Model):
    CATEGORY=(
        ('Social','Social'),
        ('Pastoral','Pastoral'),
        ('Youth','Youth'),
        ('Adult','Adult'),
    )

    depname=models.CharField(max_length=200 ,null=True)
    christian=models.ForeignKey(Congregants, null=True , on_delete=models.SET_NULL)
    category=models.CharField(max_length=300,null=True,choices=CATEGORY)

    def __str__(self):
        return self.depname
    class Meta:
        ordering = ['depname']

    def save_department(self):
        self.save()

    def delete_department(self):
        self.delete()

            
class Appointment(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Approved','Approved'),
    )

    appointee=models.CharField(max_length=200 ,null=True)
    reason=models.CharField(max_length=300,null=True)
    Date=models.DateField(auto_now_add=True,null=True)
    phoneNumber=models.CharField(max_length=20, null=True)
    comment= models.CharField(max_length=500,null=True,blank=True)
    status=models.CharField(max_length=300,null=True,choices=STATUS, default='Pending')
   
    def __str__(self):
        return self.appointee
    class Meta:
        ordering = ['Date']

    def save_appointment(self):
        self.save()

    def delete_appointment(self):
        self.delete()

        
class Wedding(models.Model):

    STATUS=(

         ('Pending','Pending'),
         ('Approved','Approved'),
     )

    groomName=models.CharField(max_length=200, null=True)
    brideName=models.CharField(max_length=200, null=True)
    phone=models.CharField(null=True, max_length=20)
    date=models.DateField(blank=True, null=True)
    status=models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    comment=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.groomName
    class Meta:
        ordering = ['groomName']

    def save_wedding(self):
        self.save()

    def delete_wedding(self):
        self.delete()


class Parish(models.Model):

    LOCATION=(
       ('Rwanda','Rwanda'),
        ('Diaspora','Diaspora'),

    )

    name=models.CharField(max_length=200, null=True)
    leader=models.ForeignKey( User, max_length=500,null=True, on_delete=models.SET_NULL)
    location=models.CharField(max_length=200, null=True, choices=LOCATION)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

    def save_parish(self):
        self.save()

    def delete_parish(self):
        self.delete()   

class Sermon(models.Model):

    description=models.CharField(max_length=200, null=True)
    uploader=models.ManyToManyField( User)
    date_added=models.DateField(auto_now_add=True, null=True)
    

    def __str__(self):
        return self.date_added
    class Meta:
        ordering = ['date_added']

    def save_sermon(self):
        self.save()

    def delete_sermon(self):
        self.delete()   

class Give(models.Model):

    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(max_length=50, null=True, blank=True)
    phone=models.CharField(max_length=50, null=True, blank=True)
    amount=models.FloatField(blank=True, null=True)
    date=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

    def save_give(self):
        self.save()

    def delete_give(self):
        self.delete()   

 











    





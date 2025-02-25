from django.db import models
from django.contrib.auth.models import User
from datetime import date
class Vanue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True)
    map_reference = models.CharField(max_length=50)
    owner = models.IntegerField("Vanue Owner", blank=False, default=1)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name 
    
class MyUser(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
  
  

    def __str__(self):
        return self.firstname + " " + self.lastname 
 

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vanue = models.ForeignKey(Vanue, on_delete=models.CASCADE, related_name='event')
    attend = models.ManyToManyField(MyUser, blank=True)
    aproved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @property 
    def days_till(self):
        today = date.today()
        till_days = self.date.date() - today
        days = str(till_days).split(",",1)[0]
        return days 
    @property
    def day(self):
        day = date.today()
        return day

    

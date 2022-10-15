from django.db import models
from datetime import datetime
# Create your models here.

class Festival(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=128)
    def __str__(self):
        return "{} {} {}".format(self.name, self.date, self.location)

#https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    
class Ticket(models.Model):
    category = models.CharField(max_length=32)
    valid_from = models.IntegerField()
    valid_to = models.IntegerField()
    iteration = models.ForeignKey('Festival', on_delete=models.CASCADE)
    username = models.CharField(max_length=128)
    
class Podium(models.Model):
    seat_limit = models.IntegerField()
    name =  models.CharField(max_length=128)

class Performance(models.Model):
    artist = models.CharField(max_length=128)
    arrives = models.DateTimeField(default=datetime.now)
    performance_time = models.DateTimeField(default=datetime.now)
    festival_iteration =  models.ForeignKey('Festival', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    podium = models.ForeignKey('Podium', on_delete=models.CASCADE)

class Genre(models.Model):
    name = models.CharField(max_length=128)
    
class Staff(models.Model):
    first_name =models.CharField(max_length=128)
    last_name =models.CharField(max_length=128)
    role =models.CharField(max_length=128)
    iteration = models.ForeignKey('Festival', on_delete=models.CASCADE)
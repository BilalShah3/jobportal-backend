from datetime import *
import geocoder
import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

# Create your models here.
class JobType(models.TextChoices):
      Permanent = 'Permanent'
      Contract = 'Contract'
      Internship = 'Internship'

class EducationLevel(models.TextChoices):  
      Diploma= 'Diploma'
      Bachelors = 'Bachelors'
      Masters = 'Masters'
      Phd = 'Phd'

class Industry(models.TextChoices):  
      Business= 'Business'
      IT = 'Information Technology'
      Banking = 'Banking'
      Phd = 'Education/Training'
      Telecommunication = 'Telecommunication'
      Others = 'Others'

class Experience(models.TextChoices):  
      NO_EXPERIENCE = 'No Experience'
      ONE_YEAR = '1 Years'
      TWO_YEAR = '2 Years'
      THREE_YEAR = '3 Years'
      FIVE_YEAR_PLUS = '5 Years above'

def return_Date_time():
    now = datetime.now()
    return now + timedelta(days=10)

class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=True)
    jobType = models.CharField(
        max_length = 10,
        choices = JobType.choices,
        default = JobType.Permanent
    )
    education = models.CharField(
        max_length = 10,
        choices = EducationLevel.choices,
        default = EducationLevel.Bachelors
    )
    industry = models.CharField(
        max_length = 30,
        choices = Industry.choices,
        default = Industry.Business
    )
    experience = models.CharField(
        max_length = 20,
        choices = Experience.choices,
        default = Experience.NO_EXPERIENCE
    )
    salary = models.IntegerField(default=1, validators = [MinValueValidator(1), MaxValueValidator(1000000)])
    positions = models.IntegerField(default=1)
    company = models.CharField(max_length=100, null=True)
    point = gismodels.PointField(default=Point(0.0,0.0))
    last_date = models.DateTimeField(default=return_Date_time)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.title

    def save(self, *args, **kwargs):
        # generating coordinates of a given address and assign to point field before saving the job 
        g = geocoder.mapquest(self.address, key=os.environ.get('GEOCODER_API'))
       
        lng = g.lng
        lat = g.lat

        self.point = Point(lng, lat)
        
        # Call the parent class's save method to actually save the object
        super(Job, self).save(*args, **kwargs)

class CandidatesApplied(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resume = models.CharField(max_length=200)
    appliedAt = models.DateTimeField(auto_now_add=True)


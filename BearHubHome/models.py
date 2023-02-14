from django.db import models
class Student(models.Model):
    First_name = models.CharField(max_length=64)
    Last_name = models.CharField(max_length=64)
    grade_level = models.IntegerField()
    password= models.CharField(max_length=64)
    points = models.IntegerField()
# Create your models here.

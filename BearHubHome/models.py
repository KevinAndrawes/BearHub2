from django.db import models
class Student(models.Model):
    First_name = models.CharField(max_length=64)
    Last_name = models.CharField(max_length=64)
    grade_level = models.IntegerField()
    password= models.CharField(max_length=64)
    points = models.IntegerField()
class Event(models.Model):
    name= models.CharField(max_length=64)
    date = models.DateField(max_length=24)
    point_value= models.IntegerField()
    students = models.ManyToManyField(Student, blank=True,related_name="event")
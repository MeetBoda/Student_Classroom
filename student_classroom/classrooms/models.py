from django.db import models

# Create your models here.

class Classrooms(models.Model):
    classroom_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'classrooms'


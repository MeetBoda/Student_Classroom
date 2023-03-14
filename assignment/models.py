from django.db import models
from classes.models import Classrooms
from users.models import Users


# Create your models here.
class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    assignment_title = models.TextField()
    assignment = models.FileField(upload_to="assignments/")
    deadline = models.DateField()
    max_marks = models.IntegerField()

    class Meta:
        db_table = 'assignments'

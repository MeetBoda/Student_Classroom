from django.db import models
from users.models import Users
from classes.models import Classrooms
from assignment.models import Assignment

# Create your models here.
class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now=True)
    work = models.FileField(upload_to="submissions/")
    marks_obtained = models.IntegerField(null=True)

    class Meta:
        db_table = 'submissions'

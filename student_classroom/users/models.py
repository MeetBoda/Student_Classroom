from django.db import models

# Create your models here.
Role = (
    ("1","Teacher"),
    ("2","Student"),
)

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=Role, default="2")

    class Meta:
        db_table = 'users'
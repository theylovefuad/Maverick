from django.db import models
from .forms import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.IntegerField

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, default="")
    subject = models.CharField(max_length=100, default="")
    desc = models.CharField(max_length=6000, default="")


    def __str__(self):
        return self.name

class UserAI(models.Model): # user additional information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    businessname = models.CharField(max_length=30)
    objective = models.CharField(max_length=30)
    sticknote = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username



class token(models.Model):
    randomToken = models.IntegerField(unique = True)
    phoneNum = models.IntegerField(default = 0, null = True)
    addNote = models.CharField(max_length = 20, default = '', null = True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, blank = False)
    completed = models.BooleanField(default = False)
    rejected = models.BooleanField(default = False)


    def __str__(self):
        return str(self.randomToken)+" "+ str(self.vendor.username)

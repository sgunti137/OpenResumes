from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Resume(models.Model):
    name = models.CharField(max_length = 40)
    rFile = models.FileField(blank = True, null = True, upload_to = 'data')
    pdfFile = models.CharField(max_length = 40)
    latexFile = models.CharField(max_length = 40)

    def __str__(self):
        return self.name

class User_resume_relation(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    resumes = models.ManyToManyField(Resume)


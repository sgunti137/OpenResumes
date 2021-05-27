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

    def __str__(self):
        return self.user.first_name
class Education(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    mtechBoard = models.CharField(max_length=50)
    mtechGrade = models.CharField(max_length=10)
    mtechYear = models.CharField(max_length=20)
    btechBoard = models.CharField(max_length=50)
    btechGrade = models.CharField(max_length=10)
    btechYear = models.CharField(max_length=20)
    ssBoard = models.CharField(max_length=50)
    ssGrade = models.CharField(max_length=10)
    ssYear = models.CharField(max_length=20)
    sBoard = models.CharField(max_length=50)
    sGrade = models.CharField(max_length=10)
    sYear = models.CharField(max_length=20)
    def str(self):
        return self.resume

class Projects(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    proTitle = models.CharField(max_length=50)
    proDate = models.CharField(max_length=20)
    clubName = models.CharField(max_length=40)
    githubLink = models.CharField(max_length=40)
    proDes = models.TextField()
    def str(self):
        return self.proTitle

class Techskills(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    pLanguages = models.CharField(max_length=100)
    webTechs = models.CharField(max_length=100)
    dbms = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    miscellaneous = models.CharField(max_length=100)
    others = models.CharField(max_length=100)
    def str(self):
        return self.resume

class Por(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    por = models.CharField(max_length=100)
    porDesc = models.TextField()
    def str(self):
        return self.resume              




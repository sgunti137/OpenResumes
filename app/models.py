from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Resume(models.Model):
    name = models.CharField(max_length = 40)
    pdfFile = models.CharField(max_length = 40)
    latexFile = models.CharField(max_length = 40)
    date = models.CharField(max_length = 30)

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
    def __str__(self):
        return self.resume

class Projects(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    proTitle = models.CharField(max_length=50)
    proDate = models.CharField(max_length=20)
    clubName = models.CharField(max_length=40)
    githubLink = models.CharField(max_length=40)
    proDes = models.TextField()
    def __str__(self):
        return self.proTitle

class Techskill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length = 60)
    value = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.resume) + '_'+str(self.name)


class Por(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    por = models.CharField(max_length=100)
    porDesc = models.TextField()
    def __str__(self):
        return self.resume
class Profile(models.Model):
    resume = models.OneToOneField(Resume,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)
    roll=models.CharField(max_length=40,null=True)
    stream=models.CharField(max_length=50,null=True)
    programme=models.CharField(max_length=50,null=True)
    minor=models.CharField(max_length=50,null=True)
    webmail=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=50,null=True)
    linkedIn=models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.resume.name)


class Experience(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE)
    exp=models.CharField(max_length=60,null=True)
    expDes=models.TextField(null=True)
    def __str__(self):
        return self.exp


class Achievement(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE)
    ach=models.CharField(max_length=60,null=True)
    achDes=models.TextField(null=True)
    def __str__(self):
        return self.ach     


class Course(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.name    
    




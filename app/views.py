# utility imports
from pathlib import Path
import os
from django.shortcuts import render
from django.http import HttpResponse
from app.tex_gen import createTextFile
from app.data_gen import data_generator
from openresume.settings import BASE_DIR,MEDIA_ROOT,MEDIA_URL
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# model imports
from app.models import *
from django.contrib.auth.models import User


# Create your views here.

@login_required()
def index(request,pk):
   
    #*********************************************
    my_dict = {}
    #*********************************************
    us = User.objects.get(username = request.user)
    resume_mod = Resume.objects.get(id=pk)
    resume_file_name = str(resume_mod.rFile)

    
    print(resume_file_name)
    if resume_file_name != "emptyFile9989898998989.txt":
        data_file_lines = open(os.path.join(MEDIA_ROOT, resume_file_name), 'r').readlines()
        for line in data_file_lines:
            if line == "":
                continue
            tmp = line.split('#')
            if len(tmp) != 2:
                continue
            my_dict[str(tmp[0])] = str(tmp[1])
    
    #************************************
    if request.method == 'POST':
        md = request.POST
        
        print(md) 
        
        education=[]
        internships=[]
        projects=[]
        # techskills=[]
        course=[]
        por=[]
        achievements=[]
        
        # edu_list = ['BTech','Seniory Secondary','Secondary']
        
        i=1
        while i:
           l =[]
        #    str0 = edu_list[i-1]
           str1 = 'Board' + str(i)
           str2 = 'Grade' + str(i)
           str3 = 'Year' + str(i)
           
           if str1 in md.keys():
               l.append('Btech')
               l.append(md[str1])
               l.append(md[str2])
               l.append(md[str3])
               education.append(l)
           else:
               break
           i=i+1
           
        
           
        i=1
        while i:
           l =[]
           str1 = 'Company' + str(i)
           str2 = 'JobDescription' + str(i)
           
           if str1 in md.keys():
               l.append(md[str1])
               l.append(md[str2])
               internships.append(l)
           else:
               break
           i=i+1
           
        i=1
        while i:
           l =[]
           str1 = 'ProTitle' + str(i)
           str2 = 'ProDate' + str(i)
           str3 = 'ClubName' + str(i)
           str4 = 'GithubLink' +str(i)
           str5 = 'ProDes' + str(i)
           
           
           if str1 in md.keys():
               l.append(md[str1])
               l.append(md[str2])
               l.append(md[str3])
               l.append(md[str4])
               l.append(md[str5])    
               projects.append(l)
           else:
               break
           i=i+1
           
        i=1
        while i:
        #    l =[]
           str1 = 'course' + str(i)
           
           if str1 in md.keys():
               course.append(md[str1])    
            #    course.append(l)
           else:
               break
           i=i+1
           
        i=1
        while i:
           l =[]
           str1 = 'por' + str(i)
           str2 = 'porDesc' + str(i)
           
           
           if str1 in md.keys():
               l.append(md[str1])
               l.append(md[str2])    
               por.append(l)
           else:
               break
           i=i+1
           
        i=1
        while i:
           l =[]
           str1 = 'ach' + str(i)
           str2 = 'achDes' + str(i)
           
           
           if str1 in md.keys():
               l.append(md[str1])
               l.append(md[str2])    
               achievements.append(l)
           else:
               break
           i=i+1
               
                
            
        

        createTextFile(name = md['name'], rollno=str(md['roll']), stream = md['stream'],branch=md['programme'],minor=md['minor'],college="IITG",
            email= md['email'],iitgmail=md['webmail'],mobileno= str(md['mobile']),
            linkedin= md['linkedIn'],
            education=education,
            internships=internships,
            projects=projects,
            techskills=[md['pLanguages'],md['webTechs'],md['dbms'],md['os'],md['miscellaneous'],md['otherSkills']],
            keyCourses=course,
            por=por,
            achievements=achievements)

        # data_generator(md,resume_file_name)
        

        os.system("pdflatex latexFile.tex")
        os.system("move latexFile.pdf ./static/pdfs")
        # #return render(request,'pdfgen/results.html',context=my_dict)
        return redirect('/results/'+str(pk)+'/')
       
    return render(request,'pdfgen/index.html',context = my_dict)




@login_required()
def results(request,pk):
    resume_mod = Resume.objects.get(id=pk)
    resume_file_name = str(resume_mod.rFile)
    results_dict = {"file_name":resume_file_name,}
    return render(request,'pdfgen/results.html',context = results_dict)

@login_required()
def home(request):

    us = User.objects.get(username = request.user)
    res_rel = us.user_resume_relation_set.first()
    resumes_list = list(Resume.objects.filter(user_resume_relation = res_rel))

    print(type(res_rel))
    

    print(Resume.objects.filter(user_resume_relation = res_rel))
    home_dict = {"name":us.first_name}
    home_dict["Resumes"] = resumes_list
    
    # if len(resumes_list)==0:
    #     return redirect('index/')

    if request.method == 'POST':
        requestDir = request.POST
        if requestDir["newResume"]=="":
            res_id = requestDir['resume_id']
            redirect_url = '/index/'+str(res_id)+'/'
            """
            resume_file_name = str(Resume.objects.get(id = res_id).rFile)
            print(resume_file_name)
            """
            return redirect(redirect_url)
        else:
            #creating a new instance and setting the parameters when ever a user request for new resume generation..
            resume_mod = Resume()
            resume_mod.name = requestDir["newResume"]
            resume_mod.save()
            resume_id = resume_mod.id

            
            new_data_file_name = 'datafile_'+str(resume_id)+'.txt'
            open(os.path.join(MEDIA_ROOT,new_data_file_name),'w').close()
            


            resume_mod = Resume.objects.get(id = resume_id)
            resume_mod.rFile.name = new_data_file_name
            resume_mod.save()
    
            res_rel.resumes.add(resume_mod)

            redirect_url = '/index/'+str(resume_mod.id)+'/'
            print(redirect_url)
            return redirect(redirect_url)

    return render(request,'pdfgen/home.html',context = home_dict)


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

        createTextFile(name = md['name'], rollno=str(md['roll']), stream = md['stream'],branch=md['programme'],minor=md['minor'],college="IITG",
            email= md['email'],iitgmail=md['webmail'],mobileno= str(md['mobile']),
            linkedin= md['linkedIn'],
            education=[["B.Tech",md['btechBoard'],md['btechGrade'],md['btechYear']],["Senior secondary",md['ssBoard'],md['ssGrade'],md['ssYear']],["Secondary",md['sBoard'],md['sGrade'],md['sYear']]],
            internships=[[md['exp1'],md['expDes1']],[md['exp2'],md['expDes2']],[md['exp3'],md['expDes3']],[md['exp4'],md['expDes4']]],
            projects=[[md['proTitle1'],md['clubName1'],md['proDes1'],md['githubLink1'],md['proDate1']],[md['proTitle2'],md['clubName2'],md['proDes2'],md['githubLink2'],md['proDate2']],[md['proTitle3'],md['clubName3'],md['proDes3'],md['githubLink3'],md['proDate3']],[md['proTitle4'],md['clubName4'],md['proDes4'],md['githubLink4'],md['proDate4']]],
            techskills=[md['pLanguages'],md['webTechs'],md['dbms'],md['os'],md['miscellaneous'],md['otherSkills']],
            keyCourses=[md['course1'],md['course2'],md['course3'],md['course4'],md['course5'],md['course6'],md['course7'],md['course8']],
            por=[[md['por1'],md['porDesc1']],[md['por2'],md['porDesc2']],[md['por3'],md['porDesc3']],[md['por4'],md['porDesc4']]],
            achievements=[[md['ach1'],md['achDes1']],[md['ach2'],md['achDes2']],[md['ach3'],md['achDes3']],[md['ach4'],md['achDes4']],[md['ach5'],md['achDes5']],[md['ach6'],md['achDes6']]]) 

        data_generator(md,resume_file_name)
        

        os.system("pdflatex latexFile.tex")
        os.system("move latexFile.pdf ./static/pdfs")
        #return render(request,'pdfgen/results.html',context=my_dict)
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
    
    if len(resumes_list)==0:
        return redirect('index/')

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


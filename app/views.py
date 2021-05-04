# utility imports
from pathlib import Path
import os
from django.shortcuts import render
from django.http import HttpResponse
from app.tex_gen import createTextFile
from app.data_gen import data_generator
from openresume.settings import BASE_DIR,MEDIA_ROOT,MEDIA_URL,STATIC_DIR
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# model imports
from app.models import *
from django.contrib.auth.models import User

#path declarations

DATA_ROOT = os.path.join(MEDIA_ROOT,'data')
LATEX_ROOT = os.path.join(STATIC_DIR,'latex')
PDFS_ROOT = os.path.join(STATIC_DIR,'pdfs')
# Create your views here.

#classes

class projectObj:
    def __init__(self, title_string, date_string,club_string, github_string, des_string, title, date, club, github, des,ind):
        self.title_string = title_string
        self.date_string = date_string
        self.club_string = club_string
        self.github_string = github_string
        self.des_string = des_string
        self.title = title
        self.date = date
        self.club = club
        self.github = github
        self.des = des
        self.ind = ind

class porObj:
    def __init__(self,por_string,por_des_string,ind,Por,PorDesc):
        self.por_string = por_string
        self.por_des_string = por_des_string
        self.ind = ind
        self.Por = Por
        self.PorDesc = PorDesc


class achObj:
    def __init__(self,ach_string,ach_des_string,ind,Ach,AchDes):
        self.ach_string = ach_string
        self.ach_des_string = ach_des_string
        self.ind = ind
        self.Ach = Ach
        self.AchDes = AchDes

class expObj():
    def __init__(self,exp_string,exp_des_string,ind,Exp,ExpDes):
        self.exp_string = exp_string
        self.exp_des_string = exp_des_string
        self.ind = ind
        self.Exp = Exp
        self.ExpDes = ExpDes

class courseObj:
    def __init__(self, course_string,Course):
        self.course_string = course_string
        self.Course = Course




@login_required()
def index(request,pk):
   
    #*********************************************
    my_dict = {}
    #*********************************************
    us = User.objects.get(username = request.user)
    resume_mod = Resume.objects.get(id=pk)
    resume_file_name = str(resume_mod.rFile)



    data_file_lines = open(os.path.join(DATA_ROOT,resume_file_name),'r').readlines()
    projectsCount = 0
    coursesCount = 0
    porCount = 0
    achCount = 0
    expCount = 0


    for line in data_file_lines:
        if line != "":
            tmp = line.split('#')
            if len(tmp) != 2:
                continue
            tmp_key = str(tmp[0])
            my_dict[tmp_key] = str(tmp[1])
            

            if "course" in tmp_key:
                coursesCount +=1
            elif "proTitle" in tmp_key and len(tmp_key) == 9:
                projectsCount +=1
            elif "por" in tmp_key and len(tmp_key) == 4:
                porCount +=1
            elif "ach" in tmp_key and len(tmp_key) == 4:
                achCount += 1
            elif "exp" in tmp_key and len(tmp_key) == 4:
                expCount +=1
    
    my_dict["projectsCount"] = projectsCount
    my_dict["porCount"] = porCount
    my_dict["coursesCount"] = coursesCount
    my_dict["achCount"] = achCount
    my_dict["expCount"] = expCount

    """
    proTitle3#
    proDate3#
    clubName3#
    githubLink3#
    proDes3#
    """


    project_list = []
    exp_list = []
    courses_list = []
    ach_list = []
    por_list = []

    #print("projectCount: ", projectsCount)
    for i in range(projectsCount):
        title_string = "proTitle" + str(i+1)
        date_string = "proDate" + str(i+1)
        club_string = "clubName" + str(i+1)
        github_string = "githubLink" + str(i+1)
        des_string = "proDes" + str(i+1)

        project_list.append(projectObj(title_string, date_string, club_string, github_string, des_string, my_dict[title_string], my_dict[date_string], my_dict[club_string], my_dict[github_string], my_dict[des_string],i+1))
    my_dict["project_list"] = project_list
 
    for i in range(porCount):
        por_string = "por" + str(i+1)
        por_des_string = "porDesc" + str(i+1)
        por_list.append(porObj(por_string,por_des_string, i+1, my_dict[por_string], my_dict[por_des_string]))
    my_dict["por_list"] = por_list

    
    for i in range(achCount):
        ach_string = "ach" + str(i+1)
        ach_des_string = "achDes" + str(i+1)
        ach_list.append(achObj(ach_string,ach_des_string,i+1,my_dict[ach_string],my_dict[ach_des_string]))
    my_dict["ach_list"] = ach_list

    
    for i in range(coursesCount):
        course_string = "course" + str(i+1)
        courses_list.append(courseObj(course_string,my_dict[course_string]))
    my_dict["courses_list"] = courses_list

    
    for i in range(expCount):
        exp_string = "exp" + str(i+1)
        exp_des_string = "expDes" + str(i+1)
        exp_list.append(expObj(exp_string,exp_des_string, i+1,my_dict[exp_string],my_dict[exp_des_string]))
    my_dict["exp_list"] = exp_list


    #the name of the pdf to be passed for displaying in the top
    pdf_string = 'pdfs/' + str(resume_mod.pdfFile)
    my_dict['pdf_string'] = pdf_string

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




        
        education = [
                     ["M.Tech",md["mtechBoard"], md["mtechGrade"],md["mtechYear"]],
                     ["B.Tech",md["btechBoard"],md["btechGrade"],md["btechYear"]],
                     ["Secondary senior",md["ssBoard"],md["ssGrade"],md["ssYear"]],
                     ["Secondary",md["sBoard"],md["sGrade"],md["sYear"]],
                    ]

        #collecting internships data     
        i=1
        while i:
           str1 = 'exp' + str(i)
           str2 = 'expDes' + str(i)
           
           if str1 in md.keys():
               internships.append([md[str1],md[str2]])
           else:
               break
           i=i+1
        
        #collecting projects data
        i=1
        while i:
           l =[]
           str1 = 'proTitle' + str(i)
           str2 = 'proDate' + str(i)
           str3 = 'clubName' + str(i)
           str4 = 'githubLink' +str(i)
           str5 = 'proDes' + str(i)
           
           
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
        
        #collecting course data
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
        
        #collecting por data
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
        
        #collecting ach data
        i=1
        while i:
           str1 = 'ach' + str(i)
           str2 = 'achDes' + str(i)

           if str1 in md.keys():   
               achievements.append([md[str1], md[str2]])
           else:
               break
           i=i+1
               
                
        createTextFile(latex_file_name = str(resume_mod.latexFile), name = md['name'], rollno=str(md['roll']), stream = md['stream'],branch=md['programme'],minor=md['minor'],college="IITG",
            email= md['email'],iitgmail=md['webmail'],mobileno= str(md['mobile']),
            linkedin= md['linkedIn'],
            education=education,
            internships=internships,
            projects=projects,
            techskills=[md['pLanguages'],md['webTechs'],md['dbms'],md['os'],md['miscellaneous'],md['otherSkills']],
            keyCourses=course,
            por=por,
            achievements=achievements)

        data_generator(md,resume_file_name)
        
        pdflatex_cmd_str = 'pdflatex '+ '-output-directory=' + str(PDFS_ROOT)+ ' ' + str(LATEX_ROOT) +'\\'+ str(resume_mod.latexFile)
        
        print(pdflatex_cmd_str)
        
        os.system(pdflatex_cmd_str)
        return redirect('/results/'+str(pk)+'/')
       
    return render(request,'pdfgen/index.html',context = my_dict)




@login_required()
def results(request,pk):
    resume_mod = Resume.objects.get(id=pk)
    #pdf_location = '{% static \'pdfs/'+str(resume_mod.pdfFile)+ '\' %}'
    pdf_loc = '/pdfs/' + str(resume_mod.pdfFile)
    latex_loc = '/latex/'+str(resume_mod.latexFile)
    results_dict = {
                    "pdf_loc": pdf_loc,
                    'latex_loc':latex_loc,
                    }
    return render(request,'pdfgen/results.html',context = results_dict)

@login_required()
def home(request):

    us = User.objects.get(username = request.user)
    res_rel = us.user_resume_relation_set.first()
    resumes_list = list(Resume.objects.filter(user_resume_relation = res_rel))

    home_dict = {"name":us.first_name}
    home_dict["Resumes"] = resumes_list
    
    # if len(resumes_list)==0:
    #     return redirect('index/')

    if request.method == 'POST':
        requestDir = request.POST
        if requestDir["newResume"]=="":
            res_id = requestDir['resume_id']
            redirect_url = '/index/'+str(res_id)+'/'
            return redirect(redirect_url)
        else:
            #creating a new instance and setting the parameters when ever a user request for new resume generation..
            resume_mod = Resume()
            resume_mod.name = requestDir["newResume"]
            resume_mod.save()
            resume_id = resume_mod.id

            
            
            new_data_file_name = 'datafile_'+str(resume_id)+'.txt'
            new_pdf_file_name = 'latexFile_'+str(resume_id)+'.pdf'
            new_latex_file_name = 'latexFile_'+str(resume_id)+'.tex'
            open(os.path.join(DATA_ROOT,new_data_file_name),'w').close()
            open(os.path.join(PDFS_ROOT,new_pdf_file_name),'w').close()
            open(os.path.join(LATEX_ROOT,new_latex_file_name),'w').close()
            


            resume_mod = Resume.objects.get(id = resume_id)
            resume_mod.rFile.name = new_data_file_name
            resume_mod.pdfFile = new_pdf_file_name
            resume_mod.latexFile = new_latex_file_name

            resume_mod.save()
    
            res_rel.resumes.add(resume_mod)

            redirect_url = '/index/'+str(resume_mod.id)+'/'
            print(redirect_url)
            return redirect(redirect_url)

    return render(request,'pdfgen/home.html',context = home_dict)


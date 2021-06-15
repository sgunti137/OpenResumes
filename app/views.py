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
import platform

# import for date and time
from datetime import datetime

# model imports
from app.models import *
from .models import Experience, Projects, Profile, Course, Por, Achievement, Techskill, Education
from django.contrib.auth.models import User

#path declarations

DATA_ROOT = os.path.join(MEDIA_ROOT,'data')
LATEX_ROOT = os.path.join(STATIC_DIR,'latex')
PDFS_ROOT = os.path.join(STATIC_DIR,'pdfs')



@login_required()
def index(request,pk):
   
    # initialize the dictionary to be sent to the template.
    my_dict = {}

    if Resume.objects.filter(id = pk).count()==0:
        return render(request, 'pdfgen/wrongIndex.html')
    
    # collected the details of the user.
    us = User.objects.get(username = request.user)
    resume_mod = Resume.objects.get(id=pk)
  

    res_rel = us.user_resume_relation_set.first()
    resume_list = list(Resume.objects.filter(user_resume_relation = res_rel)) # do it again

    if resume_mod not in resume_list:
        return render(request,'pdfgen/wrongIndex.html')

    #count of each section fields to be looped in the template.

    

    project_list = list(resume_mod.projects_set.all())
    course_list = list(resume_mod.course_set.all())
    exp_list = list(resume_mod.experience_set.all())
    por_list = list(resume_mod.por_set.all())
    ach_list = list(resume_mod.achievement_set.all())
    tech_list = list(resume_mod.techskill_set.all())

    my_dict['project_list'] = project_list
    my_dict['por_list'] = por_list
    my_dict['exp_list'] = exp_list
    my_dict['course_list'] = course_list
    my_dict['ach_list'] = ach_list
    my_dict['tech_list'] = tech_list

    #profile data

    my_dict['name'] = resume_mod.profile.name
    my_dict['roll'] = resume_mod.profile.roll
    my_dict['stream'] = resume_mod.profile.stream
    my_dict['programme'] = resume_mod.profile.programme
    my_dict['minor'] = resume_mod.profile.minor
    my_dict['webmail'] = resume_mod.profile.webmail
    my_dict['email'] = resume_mod.profile.email
    my_dict['mobile'] = resume_mod.profile.mobile
    my_dict['linkedIn'] = resume_mod.profile.linkedIn

    #Education data

    my_dict['mtechBoard'] = resume_mod.education.mtechBoard
    my_dict['mtechGrade'] = resume_mod.education.mtechGrade
    my_dict['mtechYear'] = resume_mod.education.mtechYear
    my_dict['btechBoard'] = resume_mod.education.btechBoard
    my_dict['btechGrade'] = resume_mod.education.btechGrade
    my_dict['btechYear'] = resume_mod.education.btechYear
    my_dict['ssBoard'] = resume_mod.education.ssBoard
    my_dict['ssGrade'] = resume_mod.education.ssGrade
    my_dict['ssYear'] = resume_mod.education.ssYear
    my_dict['sBoard'] = resume_mod.education.sBoard
    my_dict['sGrade'] = resume_mod.education.sGrade
    my_dict['sYear'] = resume_mod.education.sYear
            
    
    #counts of section fields sent successfully
    my_dict["projectsCount"] = len(project_list)
    my_dict["porCount"] =len(por_list)
    my_dict["coursesCount"] = len(course_list)
    my_dict["achCount"] = len(ach_list)
    my_dict["expCount"] = len(exp_list)
    my_dict['techCount'] = len(tech_list)


    # the name of the pdf to be passed for displaying in the top-> initialization and added to my_dict
    pdf_string = 'pdfs/' + str(resume_mod.pdfFile)

    if os.path.getsize('static/'+pdf_string)==0:
        pdf_string = 'data/display_resume.pdf'
    
    if os.path.isfile(os.path.join(PDFS_ROOT, resume_mod.pdfFile)) == False:
        pdf_string = 'data/display_resume.pdf'
        open(os.path.join(PDFS_ROOT,resume_mod.pdfFile),'w').close()
        # print("hululu")
        
    

    my_dict['pdf_string'] = pdf_string
    my_dict['resume'] = resume_mod     

    """****************************************************************************************************************************"""


    if request.method == 'POST':
	
	now = datetime.now()
        now_date = now.strftime("%I:%M %p %B %d, %Y")
        resume_mod.date = now_date
        resume_mod.save()
	
        #input dictionary
        md = request.POST

        if(md['delete_flag']=='true'):
            del_res = resume_mod

            delete_pdf_file = str(del_res.pdfFile)
            delete_latex_file = str(del_res.latexFile)

            delete_pdf_file = 'static/pdfs/'+delete_pdf_file
            delete_latex_file = 'static/latex/'+delete_latex_file

            os.remove(delete_pdf_file)
            os.remove(delete_latex_file)
            del_res.delete()
            return redirect('/OpenResumes')


    
        
        print(md) 
        
        # initializing section lists
        education=[]
        internships=[]
        projects=[]
        course=[]
        por=[]
        achievements=[]
        
        # edu_list = ['MTech', 'BTech','Seniory Secondary','Secondary']
        education = [
                     ["M.Tech",md["mtechBoard"], md["mtechGrade"],md["mtechYear"]],
                     ["B.Tech",md["btechBoard"],md["btechGrade"],md["btechYear"]],
                     ["Secondary senior",md["ssBoard"],md["ssGrade"],md["ssYear"]],
                     ["Secondary",md["sBoard"],md["sGrade"],md["sYear"]],
                    ]
        #education update
        new_edu=resume_mod.education
        new_edu.mtechBoard = md['mtechBoard']
        new_edu.mtechGrade = md['mtechGrade']
        new_edu.mtechYear = md['mtechYear']
        new_edu.btechBoard = md['btechBoard']
        new_edu.btechGrade = md['btechGrade']
        new_edu.btechYear = md['btechYear']
        new_edu.ssBoard = md['ssBoard']
        new_edu.ssGrade = md['ssGrade']
        new_edu.ssYear = md['ssYear']
        new_edu.sBoard = md['sBoard']
        new_edu.sGrade = md['sGrade']
        new_edu.sYear = md['sYear']
        new_edu.save()
        
        if(md["mtechBoard"]=="" and md["mtechYear"]=="" and md["mtechGrade"]==""):
            education.pop(0)

        
        #collecting internships data     
        if ('exp' in request.POST.keys()):
            exp_titles = request.POST.getlist('exp')
            exp_descs = request.POST.getlist('expDes')
            prev_exp=resume_mod.experience_set.all()
            prev_exp_count=len(prev_exp)
            new_exp_count=len(exp_titles)
            for j in range(min(prev_exp_count,new_exp_count)):
                prev_exp[j].exp=exp_titles[j]
                prev_exp[j].expDes=exp_descs[j]
                prev_exp[j].save()
            if prev_exp_count>new_exp_count:
                for j in range(new_exp_count,prev_exp_count):
                    prev_exp[j].delete()
            else:
                for j in range(prev_exp_count,new_exp_count):
                    new_exp=Experience(resume=resume_mod,exp=exp_titles[j],expDes=exp_descs[j])
                    new_exp.save()
            
            
            for i in range(len(exp_titles)):
                internships.append([exp_titles[i], exp_descs[i].split('\n')])
               
               

        #collecting projects data
        #format ["title1","club1",["desc1","desc2" .. ], "link1","date1"]
        # proDes: [['pro1 des1', 'pro1 des2' .. ], ['pro2 des', 'pro2 des2' .. ], ..]

        if('proTitle' in request.POST.keys()):
            pro_titles = request.POST.getlist('proTitle')
            pro_clubs = request.POST.getlist('clubName')
            pro_descs = request.POST.getlist('proDes')
            pro_links = request.POST.getlist('githubLink')
            pro_dates = request.POST.getlist('proDate')
            prev_pro=resume_mod.projects_set.all()
            prev_pro_count=len(prev_pro)
            new_pro_count=len(pro_titles)
            for j in range(min(prev_pro_count,new_pro_count)):
                prev_pro[j].proTitle=pro_titles[j]
                prev_pro[j].proDes=pro_descs[j]
                prev_pro[j].clubName=pro_clubs[j]
                prev_pro[j].githubLink=pro_links[j]
                prev_pro[j].proDate=pro_dates[j]
                prev_pro[j].save()
            if prev_pro_count>new_pro_count:
                for j in range(new_pro_count,prev_pro_count):
                    prev_pro[j].delete()
            else:
                for j in range(prev_pro_count,new_pro_count):
                    new_pro=Projects(resume=resume_mod,proTitle=pro_titles[j],proDes=pro_descs[j],clubName=pro_clubs[j],githubLink=pro_links[j],proDate=pro_dates[j])
                    new_pro.save()
            for i in range(len(pro_titles)):
                projects.append([pro_titles[i],pro_clubs[i], pro_descs[i].split('\n'), pro_links[i], pro_dates[i]])
        
        
        #collecting course data

        if('course' in request.POST.keys()):
            course = request.POST.getlist('course')
            prev_cou=resume_mod.course_set.all()
            prev_cou_count=len(prev_cou)
            new_cou_count=len(course)

            for j in range(min(prev_cou_count,new_cou_count)):
                prev_cou[j].name=course[j]
                prev_cou[j].save()
            if prev_cou_count>new_cou_count:
                for j in range(new_cou_count,prev_cou_count):
                    prev_cou[j].delete()
            else:
                for j in range(prev_cou_count,new_cou_count):
                    new_cou=Course(resume=resume_mod,name=course[j])
                    new_cou.save()

        
        #collecting por data

        if ('por' in request.POST.keys()):
            por_titles = request.POST.getlist('por')
            por_descs = request.POST.getlist('porDesc')
            prev_por=resume_mod.por_set.all()
            prev_por_count=len(prev_por)
            new_por_count=len(por_titles)
            for j in range(min(prev_por_count,new_por_count)):
                prev_por[j].por=por_titles[j]
                prev_por[j].porDesc=por_descs[j]
                prev_por[j].save()
            if prev_por_count>new_por_count:
                for j in range(new_por_count,prev_por_count):
                    prev_por[j].delete()
            else:
                for j in range(prev_por_count,new_por_count):
                    new_por=Por(resume=resume_mod,por=por_titles[j],porDesc=por_descs[j])
                    new_por.save()

            for i in range(min(len(por_titles), len(por_descs))):
                por.append([por_titles[i], por_descs[i].split('\n') ])


        #collecting techskills

        techskills = {}
        if('tech' in request.POST.keys()):
            tech_titles = request.POST.getlist('tech')
            tech_descs = request.POST.getlist('techDes')
            prev_tech = resume_mod.techskill_set.all()
            prev_tech_count=len(prev_tech)
            new_tech_count=len(tech_titles)
            for j in range(min(prev_tech_count,new_tech_count)):
                prev_tech[j].name=tech_titles[j]
                prev_tech[j].value=tech_descs[j]
                prev_tech[j].save()
            if prev_tech_count>new_tech_count:
                for j in range(new_tech_count,prev_tech_count):
                    prev_tech[j].delete()
            else:
                for j in range(prev_tech_count,new_tech_count):
                    new_tech=Techskill(resume=resume_mod,name=tech_titles[j],value=tech_descs[j])
                    new_tech.save()

            for i in range(len(tech_titles)):
                techskills[tech_titles[i]] = tech_descs[i]
 


        
        #collecting ach data achievements = [[ach1, [achdes1, achdes2, .. ], [] , ..]]

        if('ach' in request.POST.keys()):
            ach_titles = request.POST.getlist('ach')
            ach_descs = request.POST.getlist('achDes')
            prev_ach=resume_mod.achievement_set.all()
            prev_ach_count=len(prev_ach)
            new_ach_count=len(ach_titles)
            for j in range(min(prev_ach_count,new_ach_count)):
                prev_ach[j].ach=ach_titles[j]
                prev_ach[j].achDes=ach_descs[j]
                prev_ach[j].save()
            if prev_ach_count>new_ach_count:
                for j in range(new_ach_count,prev_ach_count):
                    prev_ach[j].delete()
            else:
                for j in range(prev_ach_count,new_ach_count):
                    new_ach=Achievement(resume=resume_mod,ach=ach_titles[j],achDes=ach_descs[j])
                    new_ach.save()        
   
            for i in range(min(len(ach_titles),len(ach_descs))):
                achievements.append([ach_titles[i], ach_descs[i].split('\n')])
                


        #profile model update
        pro_model=resume_mod.profile
        print(pro_model)
        pro_model.name=md['name'] 
        pro_model.roll=md['roll']
        pro_model.stream=md['stream']
        pro_model.programme=md['programme']
        pro_model.minor=md['minor']
        pro_model.email=md['email']
        pro_model.webmail=md['webmail']
        pro_model.mobile=str(md['mobile'])
        pro_model.linkedIn=md['linkedIn']
        pro_model.save()           
        

        #generating the LaTex file 
        createTextFile(latex_file_name = str(resume_mod.latexFile), name = md['name'], rollno=str(md['roll']), stream = md['stream'],branch=md['programme'],minor=md['minor'],college="IIT Guwahati",
            email= md['email'],iitgmail=md['webmail'],mobileno= str(md['mobile']),
            linkedin= md['linkedIn'],
            education=education,
            internships=internships,
            projects=projects,
            techskills=techskills,
            keyCourses=course,
            por=por,
            achievements=achievements)

        # compiling the latex file and generating pdf file
        pdflatex_cmd_str = 'pdflatex '+ '-output-directory=' + str(PDFS_ROOT)+ ' ' + str(LATEX_ROOT) 
        
        if str(platform.system())=='Linux':
            pdflatex_cmd_str += '/'
        elif str(platform.system())=='Windows':
            pdflatex_cmd_str += '\\'
        
        pdflatex_cmd_str += str(resume_mod.latexFile)
        os.system(pdflatex_cmd_str)

        #deleting auxilary files for efficient memory usage.
        # plain_name = str(resume_mod.latexFile)
        # plain_name = 'static/pdfs/'+plain_name[:-4]
        # os.remove(plain_name + '.aux')
        # os.remove(plain_name + '.out')
        # os.remove(plain_name + '.log')
        
        return redirect('/OpenResumes/index/'+str(pk)+'/')
       
    return render(request,'app/index.html',context = my_dict)




@login_required()
def results(request,pk):
    #checking whether the requested resume is permitted for the current user
    us = User.objects.get(username = request.user)
    resume_mod = Resume.objects.get(id=pk)
    res_rel = us.user_resume_relation_set.first()
    resume_list = list(Resume.objects.filter(user_resume_relation = res_rel))

    
    if resume_mod not in resume_list:
        return render(request,'pdfgen/wrongIndex.html')

    
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
    if res_rel is None:
        res_rel = User_resume_relation()
        res_rel.user = us
        res_rel.save()
    resumes_list = list(Resume.objects.filter(user_resume_relation = res_rel))
    print(resumes_list)

    home_dict = {"name":us.first_name}
    home_dict["Resumes"] = resumes_list



    
    # if len(resumes_list)==0:
    #     return redirect('index/')

    if request.method == 'POST':
        requestDir = request.POST

        print(requestDir)
        
        if requestDir["delete_flag"]=='true':
            delete_resume_id = int(requestDir['delete_resume_id'])
            del_res = Resume.objects.get(id = delete_resume_id)

            delete_pdf_file = str(del_res.pdfFile)
            delete_latex_file = str(del_res.latexFile)

            delete_pdf_file = 'static/pdfs/'+delete_pdf_file
            delete_latex_file = 'static/latex/'+delete_latex_file

            os.remove(delete_pdf_file)
            os.remove(delete_latex_file)
            del_res.delete()
            return redirect('/OpenResumes')

	if requestDir["renameResume"]=="":
            print("rename form print...")
        else: 
            pk=requestDir["renameResumeId"]
            res_mod=Resume.objects.get(pk=pk)
            res_mod.name=requestDir["renameResume"]
            res_mod.save()
            print("saved .....")
            return redirect('/OpenResumes')
        if requestDir["newResume"]=="":
            print("form submitted successfully..")
            return redirect('/OpenResumes')
        
        if requestDir["newResume"]!="":
            #creating a new instance and setting the parameters when ever a user request for new resume generation..
            resume_mod = Resume()
            resume_mod.name = requestDir["newResume"]
            resume_mod.save()
            now = datetime.now()
            now_date = now.strftime("%I:%M %p %B %d, %Y")
            resume_mod.date = now_date
            resume_id = resume_mod.id
            resume_mod.save()

            #setting the object attributes
            
            new_pdf_file_name = str(us.last_name)+'_' + resume_mod.name.replace(' ', '_') + '.pdf'
            new_latex_file_name = str(us.last_name)+'_' + resume_mod.name.replace(' ', '_') + '.tex'
            # new_pdf_file_name = 'latexFile_'+str(resume_id)+'.pdf'
            # new_latex_file_name = 'latexFile_'+str(resume_id)+'.tex'
            open(os.path.join(PDFS_ROOT,new_pdf_file_name),'w').close()
            open(os.path.join(LATEX_ROOT,new_latex_file_name),'w').close()
            


            resume_mod = Resume.objects.get(id = resume_id)
            resume_mod.pdfFile = new_pdf_file_name
            resume_mod.latexFile = new_latex_file_name

            resume_mod.save()
            res_mod_stream = ""
            if str(us.last_name)[2]== "0":
                res_mod_stream = 'B.Tech'
            else:
                res_mod_stream = 'PG'
            pro_mod=Profile(resume=resume_mod, name = us.first_name, roll = us.last_name,
                            webmail = us.username, programme = deptList[str(us.last_name)[4:6]], stream =  res_mod_stream)
            pro_mod.save()
            # tech_mod=Techskills(resume=resume_mod)
            # tech_mod.save()
            edu_mod=Education(resume=resume_mod)
            edu_mod.save()
            res_rel.resumes.add(resume_mod)

            redirect_url = '/OpenResumes/index/'+str(resume_mod.id)+'/'
            print(redirect_url)
            return redirect(redirect_url)

    return render(request,'app/home.html',context = home_dict)


deptList ={
    '01': 'CSE',
    '02': 'ECE',
    '03': 'ME',
    '04': 'Civil',
    '05': 'Design',
    '06': 'BSBE',
    '07': 'CL',
    '08': 'EEE',
    '21': 'Physics',
    '22': 'Chemistry',
    '23': 'MNC',
    '41': 'HSS',
    '51': 'Energy',
    '52': 'Environment',
    '53': 'Nano-Tech',
    '54': 'Rural-Tech',
    '55': 'Linguistics',
	'61': 'Others',
	'62': 'Others',
	'63': 'Others',
}

"""
def send(request):
    toh=request.POST['to']
    print(toh)
    mail_content = '''
    '''
    sender_address = 'resumegenerator112@gmail.com'
    sender_pass = 'Resumegenerator123'
    receiver_address = toh
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Hi bro Nuv thoppp!!!!!!!'
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name ='static/pdfs/'+ Resume.objects.get(id=request.POST['pk']).pdfFile
    print
    attach_file = open(attach_file_name, 'rb') 
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) 
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls() 
    session.login(sender_address, sender_pass) 
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    return redirect('home')
"""

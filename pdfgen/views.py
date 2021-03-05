from django.shortcuts import render
from django.http import HttpResponse
from pdfgen.tex_gen import createTextFile
from openresume.settings import BASE_DIR
import os


# Create your views here.

def index(request):
    #print(request.GET)
    new_dict = request.POST
    
    my_dict = {}
    if request.method == 'POST':
        md = request.POST
        
        print(md)
        
        createTextFile(name = md['name'], rollno=str(md['roll']), stream = md['stream'],branch=md['programme'],minor=md['minor'],college="IITG",
            email= md['email'],iitgmail=md['webmail'],mobileno= str(md['mobile']),
            linkedin= md['linkedIn'],
            education=[["B.Tech",md['btechBoard'],md['btechGrade'],md['btechYear']],["Senior secondary",md['ssBoard'],md['ssGrade'],md['ssYear']],["Secondary",md['sBoard'],md['sGrade'],md['sYear']]],
            projects=[[md['proTitle1'],md['clubName1'],md['proDes1'],md['githubLink1'],md['proDate1']],[md['proTitle2'],md['clubName2'],md['proDes2'],md['githubLink2'],md['proDate2']],[md['proTitle3'],md['clubName3'],md['proDes3'],md['githubLink3'],md['proDate3']],[md['proTitle4'],md['clubName4'],md['proDes4'],md['githubLink4'],md['proDate4']]],
            techskills=[md['pLanguages'],md['webTechs'],md['dbms'],md['os'],md['miscellaneous'],md['otherSkills']],
            keyCourses=[md['course1'],md['course2'],md['course3'],md['course4'],md['course5'],md['course6'],md['course7'],md['course8']],
            por=[[md['por1'],md['porDesc1']],[md['por2'],md['porDesc2']],[md['por3'],md['porDesc3']],[md['por4'],md['porDesc4']]],
            achievements=[[md['ach1'],md['achDes1']],[md['ach2'],md['achDes2']],[md['ach3'],md['achDes3']],[md['ach4'],md['achDes4']],[md['ach5'],md['achDes5']],[md['ach6'],md['achDes6']]]) 
        
        
        os.system("cd")
        os.system("pdflatex latexFile.tex")
        os.system("move latexFile.pdf ./static/pdfs")
        return render(request,'pdfgen/results.html',context=my_dict)
       
    return render(request,'pdfgen/index.html',context = my_dict)



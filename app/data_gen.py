from pathlib import Path
import os
from openresume.settings import BASE_DIR,MEDIA_ROOT,STATIC_DIR

DATA_ROOT = os.path.join(MEDIA_ROOT,'data')

def data_generator(my_dic,filename, achievements, por, course, projects, internships):
    data_file_path = os.path.join(DATA_ROOT,filename)
    datafile = open(data_file_path,"w")
    
    
    #non iteratable fields hardcoded.. 
    ni_field_list = ['name', 'roll', 'mobile', 'stream', 'programme', 'webmail', 'email', 'linkedIn', 'minor',
     'mtechBoard', 'mtechGrade', 'mtechYear',
     'btechBoard', 'btechGrade', 'btechYear', 
     'ssBoard', 'ssGrade', 'ssYear', 
     'sBoard', 'sGrade', 'sYear',
     'pLanguages', 'webTechs', 'dbms', 'os', 'miscellaneous', 'otherSkills'] 

    for key in ni_field_list:
        datafile.write(key+'#'+my_dic[key] + '\n')

    #iteratable fields automated ..


    #achivements

    for i in range(len(achievements)):
        datafile.write("ach" + str(i+1) + '#' + achievements[i][0] + "\n")
        datafile.write("achDes" + str(i+1) + '#' + achievements[i][1] + "\n")

    #por 

    for i in range(len(por)):
        datafile.write("por" + str(i+1) + '#' + por[i][0] + "\n")
        datafile.write("porDesc" + str(i+1) + '#' + por[i][1] + "\n")
    
    #courses 

    for i in range(len(course)):
        datafile.write("course" + str(i+1) + '#' + course[i] + "\n")
    
    #projects

    for i in range(len(projects)):
        datafile.write("proTitle" + str(i+1) + '#' + projects[i][0] + "\n")
        datafile.write("clubName" + str(i+1) + '#' + projects[i][1] + "\n")
        datafile.write("proDes" + str(i+1) + '#' + projects[i][2] + "\n")
        datafile.write("githubLink" + str(i+1) + '#' + projects[i][3] + "\n")
        datafile.write("proDate" + str(i+1) + '#' + projects[i][4] + "\n")

    #internships

    for i in range(len(internships)):
        datafile.write("exp" + str(i+1) + '#' + internships[i][0] + "\n")
        datafile.write("expDes" + str(i+1) + '#' + internships[i][1] + "\n")

        

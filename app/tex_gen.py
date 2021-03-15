from openresume.settings import BASE_DIR
from pathlib import Path
import os
from percent_rem import percentReplacerString
from percent_rem import percentReplacerDict


def createTextFile(name,rollno,stream,branch,minor,college,email,iitgmail,mobileno,linkedin,education,projects,techskills,keyCourses,por,achievements):
    
    PDFGEN_DIR = os.path.join(BASE_DIR,'app')

    base_file_path = os.path.join(PDFGEN_DIR,"base.txt")
    latexFile_path = os.path.join(BASE_DIR,"latexFile.tex")

    readfile = open(str(base_file_path),"rt")
    writefile=open(str(latexFile_path),"w")

    lines=readfile.readlines()

    #write some static code
    for i in range(0,87):
        writefile.write(lines[i])

    #Heading Dynamic Code
    #if Minor is there 
    writefile.write(r"\textbf{\huge "+name+r"}\\")
    writefile.write("\n")

    for i in range(87,91):
        writefile.write(lines[i])

    if (minor!=""):
        writefile.write(r"{Roll No. "+rollno+r"}&\href{mailto:"+email+r"}{ "+email+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+stream+r"}& Mobile : "+mobileno+r"\\")
        writefile.write("\n")
        writefile.write(r"{"+branch+r"}&\href{mailto:"+iitgmail+r"}{ "+iitgmail+r"}\\")
        writefile.write("\n")
        writefile.write(r"{Minor in "+minor+r"} & \href{"+linkedin+r"/}{"+linkedin+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+college+r"}&{}")
        # writefile.write(r"{Minor in "+minor+r"}&{}")
    #else
    else:
        writefile.write(r"{Roll No. "+rollno+r"}&\href{mailto:"+email+r"}{ "+email+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+stream+r"}& Mobile : "+mobileno+r"\\")
        writefile.write("\n")
        writefile.write(r"{"+branch+r"}&\href{mailto:"+iitgmail+r"}{ "+iitgmail+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+college+"} & \href{"+linkedin+r"/}{"+linkedin+r"}")
        writefile.write("\n")

    #write some static code
    for i in range(96,112):
        writefile.write(lines[i])

    #Education Dynamic code
    #education=[["d1","c1","p1","y1"],["d2","c2","p2","y2"],["d3","c3","p3","y3"]]
    for sublist in education:
        if(sublist[0]!=""):
            for i in range(len(sublist)):
                sublist[i]=percentReplacerString(sublist[i])
            writefile.write(r"\hline "+sublist[0] +r"& "+sublist[1]+ r"& "+sublist[2] +r"& "+sublist[3] +r"\\")
            writefile.write("\n")
   
    #write some static code
    for i in range(115,126):
        writefile.write(lines[i])

    proFlag = False
    for sl in projects:
        if(sl[0]!=""):
            proFlag = True
            break
    if(proFlag):
        writefile.write(lines[126])
        writefile.write(lines[127])
    #Projects Dynamic code
    #projects=[["title1","club1","desc1","link1","date1"],["title2","club2","desc2","link2","date2"],["title3","club3","desc3","link3","date3"],["title4","club4","desc4","link4","date4"]]
    for sublist in projects:
        for i in range(len(sublist)):
            if(i!=3):
                sublist[i]=percentReplacerString(sublist[i])
        if(sublist[0]!="" and sublist[1]!="" and sublist[2]!="" and sublist[3]!="" and sublist[4]!=""):
            writefile.write(r"\resumeSubheading{"+sublist[0]+r"}{"+sublist[4]+r"}{"+sublist[1]+r"}{\href{"+sublist[3]+r"}{\textit{\small "+sublist[3]+r"   }}}")
            writefile.write("\n")
            writefile.write(r"\begin{itemize}")
            writefile.write("\n")
            writefile.write(r"\item "+sublist[2])
            writefile.write("\n")
            writefile.write(r" \end{itemize}")
            writefile.write("\n")
            writefile.write(r"\vspace{2pt}")
            writefile.write("\n")
            writefile.write("\n")
    
    #write some static code
    writefile.write(lines[151])
    if(proFlag):
        writefile.write(lines[152])

    for i in range(153,162):
        writefile.write(lines[i])

    tsFlag = False
    for i in techskills:
        if i!="":
            tsFlag = True
            break

    if(tsFlag):
        writefile.write(lines[162])
        writefile.write(lines[163])
    #Technical Skills Dynamic code
    #techskills=["pllang","webtech","dbms","os","miscell","otherskills"]
    for i in range(len(techskills)):
        techskills[i]=percentReplacerString(techskills[i])
    if(techskills[0]!=""):
        writefile.write(r"\resumeSubItem{Programming Languages}{"+techskills[0]+r"}")
        writefile.write("\n")
    if(techskills[1]!=""):
        writefile.write(r"\resumeSubItem{Web Technologies}{"+techskills[1]+r"}")
        writefile.write("\n")
    if(techskills[2]!=""):
        writefile.write(r"\resumeSubItem{DBMS}{"+techskills[2]+r"}")
        writefile.write("\n")
    if(techskills[3]!=""):
        writefile.write(r"\resumeSubItem{OS}{"+techskills[3]+r"}")
        writefile.write("\n")
    if(techskills[4]!=""):
        writefile.write(r"\resumeSubItem{Miscelleneous}{"+techskills[4]+r"}")
        writefile.write("\n")
    if(techskills[5]!=""):
        writefile.write(r"\resumeSubItem{Other Skills}{"+techskills[5]+r"}")
        writefile.write("\n")
    
    #write some static code
    for i in range(170,173):
        writefile.write(lines[i])
    
    if(tsFlag):
        writefile.write(lines[173])

    for i in range(174,186):
        writefile.write(lines[i])

    cFlag = False
    for course in keyCourses:
        if(course!=""):
            cFlag = True
            break
    
    if(cFlag==False):
        writefile.write(r"\item null")
    #Key courses Dynamic code
    # keyCourses=["ma101","webd101","cpp110"]
    for course in keyCourses:
        course=percentReplacerString(course)
        if(course!=""):
            writefile.write(r"\item "+course)
            writefile.write("\n")
    
    #write some static code
    for i in range(194,206):
        writefile.write(lines[i])


    porFlag = False
    for pors in por:
        if(pors[0]!=""):
            porFlag = True
            break

    if(porFlag):
        writefile.write(lines[206])
        writefile.write(lines[207])
    #POR Dynamic code
    #por=[["title1","desc1"],["title2","desc2"],["title3","desc3"],["title4","desc4"]]
    for sublist in por:
        for i in range(len(sublist)):
            sublist[i]=percentReplacerString(sublist[i])
        if(sublist[0]!=""):
            writefile.write(r"\resumeSubItem{"+sublist[0]+r"}")
            writefile.write("\n")
            writefile.write(r"{\vspace{-7pt}")
            writefile.write("\n")
            writefile.write(r"\begin{itemize}")
            writefile.write("\n")
            writefile.write(r"\item "+sublist[1])
            writefile.write("\n")
            writefile.write(r"\end{itemize} }")
            writefile.write("\n")
            writefile.write("\n")
    
    #write some static code
    writefile.write(lines[231])
    if(porFlag):   
        writefile.write(lines[232])
        writefile.write(lines[233])
    
    for i in range(234,242):
        writefile.write(lines[i])

    achFlag = False
    for ach in achievements:
        if(ach[0]!=""):
            achFlag = True
            break
    if(achFlag):
        writefile.write(lines[242])
    writefile.write(lines[243])
    #Achievements Dynamic code
    #achievements=[["title1","desc1"],["title2","desc2"],["title3","desc3"],["title4","desc4"],["title5","desc5"],["title6","desc6"]]
    for sublist in achievements:
        for i in range(len(sublist)):
            sublist[i]=percentReplacerString(sublist[i])
        if(sublist[0]!=""):
            writefile.write(r"\resumeSubItem{"+sublist[0]+r"}{"+sublist[1]+r"}")
            writefile.write("\n")
    
    #write some static code
    writefile.write(lines[250])
    if(achFlag):
        writefile.write(lines[251])
    for i in range(252,256):
        writefile.write(lines[i])



"""
createTextFile(name="Nikitha",rollno="190102052",stream="Btech",branch="ECE",minor="CSE",college="IITG",
              email="nikithareddy@gmail.com",iitgmail="m.nikitha@iitg.ac.in",mobileno="9848670705",
              linkedin="linkedin.com/in/nikitha2309",
              education=[["d1","c1","p1","y1"],["d2","c2","p2","y2"],["","","",""]],
              projects=[["title1","club1","desc1","link1","date1"],["title2","club2","desc2","link2","date2"],["title3","club3","desc3","link3","date3"],["title4","club4","desc4","link4","date4"]],
              techskills=["pllang","webtech","dbms","os","miscell","otherskills"],
              keyCourses=["ma101","webd101","cpp110"],
              por=[["title1","desc1"],["title2","desc2"],["title3","desc3"],["title4","desc4"]],
              achievements=[["title1","desc1"],["title2","desc2"],["title3","desc3"],["title4","desc4"],["title5","desc5"],["title6","desc6"]])
"""




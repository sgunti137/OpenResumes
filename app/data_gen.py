from pathlib import Path
import os
from openresume.settings import BASE_DIR,MEDIA_ROOT,STATIC_DIR

def data_generator(my_dic,filename):
    data_file_path = os.path.join(MEDIA_ROOT,filename)
    datafile = open(data_file_path,"w")
    for key in my_dic:
        if(key=="csrfmiddlewaretoken"):
            continue
        datafile.write(key+'#'+my_dic[key])
        datafile.write("\n")
    

    dfp2 = os.path.join(STATIC_DIR,'data/datafile.txt')
    df = open(dfp2,"w")
    for key in my_dic:
        if(key=="csrfmiddlewaretoken"):
            continue
        df.write(key+'#'+my_dic[key])
        df.write('\n')
   


from pathlib import Path
import os
from openresume.settings import BASE_DIR,MEDIA_ROOT,STATIC_DIR

DATA_ROOT = os.path.join(MEDIA_ROOT,'data')

def data_generator(my_dic,filename):
    data_file_path = os.path.join(DATA_ROOT,filename)
    datafile = open(data_file_path,"w")
    for key in my_dic:
        if(key=="csrfmiddlewaretoken" or key=="save_flag"):
            continue
        datafile.write(key+'#'+my_dic[key])
        datafile.write("\n")
   


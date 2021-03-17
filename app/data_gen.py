from pathlib import Path
import os
from openresume.settings import BASE_DIR

def data_generator(my_dic):
    data_file_path = os.path.join(BASE_DIR,"datafile.txt")
    datafile = open(str(data_file_path),"w")
    for key in my_dic:
        if(key=="csrfmiddlewaretoken"):
            continue
        datafile.write(key+'#'+my_dic[key])
        datafile.write("\n")


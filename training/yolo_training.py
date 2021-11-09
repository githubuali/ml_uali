import numpy as np
import os
import json
from gen_txt import gen_txt


def count_classes(input):
    """ Función que devuelve una lista en donde aparecen ordenados la cantidad 
    de veces que aparece cada clase en todo el dataset.
    * Args: 
        * input (JSON)
    * output:
        * cantidad_clases(list)
    """
    return None

def actualizar_elemento(clase, clases_elim):
    i=0
    while clase > clases_elim[i]:
        i=i+1
        if i == len(clases_elim):
            break
    return(clase-i)

def remove_class(path, clases_elim):
    """ Función que modifica el dataset eliminando las clases que quieran eliminarse,
     para eso debe pasarse el parámetro "remove_class" con una lista de las clases que 
     deseen eliminarse.
    * Args: 
        * input (JSON)
    * output:
        * None
    """
    os.system("mkdir "+path + "dataset_new/")
    for file in os.listdir(path):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"): 
            labels = open(path+filename).read().strip().split("\n")
            if labels !=['']:
                new_txt = []
                for elemento in labels: # lee cada elemento detectado de cada imagen
                    elemento = elemento.split()
                    if int(elemento[0]) not in clases_elim:
                        elemento[0]=str(actualizar_elemento(int(elemento[0]),clases_elim))                            
                        elemento= " ".join(elemento)
                        new_txt.append(elemento)
                new_txt = "\n".join(new_txt)
                outfile = open(path +"dataset_new/" + file,'w')
                outfile.write(new_txt)
                outfile.close()

    return None


def data_purge(input):
    if "remove_class" in input:
        remove_class("darknet/data/train_annot/train/", input["remove_class"])
    os.system("cp -R darknet/data/train_annot/train/dataset_new/.  darknet/data/train/")
    os.system("rm -rf darknet/data/train_annot")
    if "valid" in input:
        if "remove_class" in input:
            remove_class("darknet/data/valid_annot/valid/", input["remove_class"])
        os.system("cp -R darknet/data/valid_annot/valid/dataset_new/. darknet/data/valid")
        os.system("rm -rf darknet/data/valid_annot")
    return None


def modif_names(path, classes):
    names = open(path).read().strip().split("\n")
    for index in sorted(classes, reverse=True):
        del names[index]
    new_txt = "\n".join(names)
    outfile = open(path,'w')
    outfile.write(new_txt)
    outfile.close()
    return None
    

def download_drive(link, name, unzip=True):
    
    link = link.replace("/view?usp=sharing", "")
    os.system("""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=""" + link.split("/")[-1] + """' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*"""+ r"/\1\n/p')&id=" + link.split("/")[-1] + '" -O '+ name +'.zip && rm -rf /tmp/cookies.txt')
    if unzip==True:
        os.system("unzip "+ name +".zip -d darknet/data/"+ name)
        os.system("rm "+ name +".zip")
    return None

if __name__ == "__main__":

    """
    input_json = {
        "train":["",""],
        "valid":["",""],
        "test":["",""],
        "training_files':"",
        "flags":""
        "remove_class":[]
    }


    """

    #os.system("git clone https://github.com/AlexeyAB/darknet")
    with open("input.json") as json_file:
        input_json = json.load(json_file)

    #download_drive(input_json["train"][0],"train")
    #os.system("cp -R darknet/data/train/train/. darknet/data/train")
    #os.system("rm -rf darknet/data/train/train")
    #download_drive(input_json["train"][1],"train_annot")
    
    if "valid" in input_json:
        #download_drive(input_json["valid"][0],"valid")
        os.system("cp -R darknet/data/valid/valid/. darknet/data/valid")
        os.system("rm -rf darknet/data/valid/valid")
        download_drive(input_json["valid"][1],"valid_annot")
    #if "test" in input_json:
    #    download_drive(input_json["test"][0],"test", unzip=False)
    #    download_drive(input_json["test"][1],"test_annot",unzip=False)

    input_json["training_files"] = input_json["training_files"].replace("/view?usp=sharing", "")

    os.system("""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=""" + input_json["training_files"].split("/")[-1] + """' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*"""+ r"/\1\n/p')&id=" + input_json["training_files"].split("/")[-1] + '" -O '+ "training_files" +'.zip && rm -rf /tmp/cookies.txt')

    os.system("unzip training_files.zip")
    os.system("rm training_files.zip")
    os.system("cp "+input_json["dataset"]+"/"+input_json["version"]+"/yolov4.data darknet/data/yolov4.data")
    os.system("cp "+input_json["dataset"]+"/"+input_json["version"]+"/yolov4.names darknet/data/yolov4.names")
    os.system("cp "+input_json["dataset"]+"/"+input_json["version"]+"/yolov4.cfg darknet/cfg/yolov4.cfg")
    os.system("rm -rf "+input_json["dataset"])

    os.system("mkdir darknet/checkpoints")

    data_purge(input_json)
    gen_txt()
    #os.system("wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137")
    os.chdir("darknet/")
    os.system("sudo ./darknet detector train data/yolov4.data cfg/yolov4.cfg yolov4.conv.137 -dont_show -map")
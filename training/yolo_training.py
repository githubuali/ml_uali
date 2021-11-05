import numpy as np
import os
import json

def count_classes(input):
    """ Función que devuelve una lista en donde aparecen ordenados la cantidad 
    de veces que aparece cada clase en todo el dataset.
    * Args: 
        * input (JSON)
    * output:
        * cantidad_clases(list)
    """
    return None


def remove_class(input):
    """ Función que modifica el dataset eliminando las clases que quieran eliminarse,
     para eso debe pasarse el parámetro "remove_class" con una lista de las clases que 
     deseen eliminarse.
    * Args: 
        * input (JSON)
    * output:
        * None
    """

    return None

def download_drive(link, name, unzip=True):
    
    link = link.replace("/view?usp=sharing", "")
    os.system("""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=""" + link.split("/")[-1] + """' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*"""+ r"/\1\n/p')&id=" + link.split("/")[-1] + '" -O '+ name +'.zip && rm -rf /tmp/cookies.txt')
    if unzip==True:
        os.system("unzip "+ name +".zip -d darknet/data/")
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
    download_drive(input_json["train"][1],"train_annot")
    
    if "valid" in input_json:
        download_drive(input_json["valid"][0],"valid")
        download_drive(input_json["valid"][1],"valid_annot")
    if "test" in input_json:
        download_drive(input_json["test"][0],"test", unzip=False)
        download_drive(input_json["test"][1],"test_annot",unzip=False)
    

    


# -*- coding: utf-8 -*-

"""
visdroneToYolo is a script to transform the labels from one dataset to another

##################################################
## Author: Maxi
## Version: 1.0
## Status: developing
##################################################
"""

import warnings
import numpy as np
import glob
import cv2
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
import logging

abs_path = os.path.dirname(os.path.abspath(__file__))

def richMessage (message, Type):
    """ 

    Arg:

    Returns: 

    Example:

    Reference: 
        * Format color: https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    """
    
    if Type == 'warning':
        title = '[WARNING]'
        color = ['\x1b[0;30;43m','\x1b[0m']

    elif Type == 'error':   
        title = '[ERROR]'
        color = ['\x1b[0;30;41m','\x1b[0m']

    else:
        print ('undefined type !')

    msj_Type = color[0] + title + color[1] + ' - '

    return print(msj_Type + message)

def getImageDim (path):
    """ 

    Arg:

    Returns: 

    Example:

    """
    
    images_paths = sorted(glob.glob(path + "/*.jpg"))
    imagesDim = []
    for img in tqdm(images_paths, desc="Getting image dimensions"):
        try:
            images = cv2.imread(img)
            imagesDim.append ((images.shape[1],images.shape[0]))
        except:
                richMessage ('Converting valid annotations error, image: '+ paths_annos[i], 'warning')
                continue

    return np.array(imagesDim) 

def getAnnotations(path):
    """ 

    Arg:

    Returns: 

    Example:

    """  

    paths_annos = sorted(glob.glob(path+ "/*.txt"))

    anno_list = []
    for anno_file in paths_annos:
        anno_list.append(np.loadtxt(anno_file, dtype=np.float32, delimiter=",", usecols=(5,0,1,2,3), ndmin=2))  # ndim = 2, for images with a single label
    return np.array(anno_list), paths_annos

def visDroneToYolo (path_images, path_annos):
    """ 

    Arg:

    Returns: 

    Example:

    """

    imagesDim = getImageDim (path_images)
    annos, paths_annos = getAnnotations(path_annos)

    for i in tqdm(range(len(annos)), desc="Converting valid annotations"):
        s = annos[i].shape
        if len(s) == 1:
            try:
                    annos[i][1] = annos[i][1] + annos[i][3]/2
                    annos[i][2] = annos[i][2] + annos[i][4]/2
                    annos[i][1] /= imagesDim[i][0]
                    annos[i][2] /= imagesDim[i][1]
                    annos[i][3] /= imagesDim[i][0]
                    annos[i][4] /= imagesDim[i][1]
            except:
                    richMessage ('Converting valid annotations error, image: '+ paths_annos[i], 'warning')
                    continue
        elif len(s) == 2:
            for j in range(len(annos[i])):
                try:
                    annos[i][j][1] = annos[i][j][1] + annos[i][j][3]/2
                    annos[i][j][2] = annos[i][j][2] + annos[i][j][4]/2
                    annos[i][j][1] /= imagesDim[i][0]
                    annos[i][j][2] /= imagesDim[i][1]
                    annos[i][j][3] /= imagesDim[i][0]
                    annos[i][j][4] /= imagesDim[i][1]
                except:
                    richMessage ('Converting valid annotations error, image: '+ paths_annos[i], 'warning')
                    continue
   
    for i, path_annos in tqdm(enumerate(paths_annos), desc="Save new annotations"):
            np.savetxt(path_annos, annos[i], fmt='%d %f %f %f %f')

def drawBoundingBox_visDrone(image, annotation, object_category):
    """ 

    Arg:

    Returns: 

    Example:

    """

    img = cv2.imread(image)
    image_h, image_w, _  = img.shape

    fl = open(annotation, 'r')
    boxes = fl.readlines()
    fl.close()
    
    for box in boxes:
        # Split string to float
        bbox_left, bbox_top, bbox_width, bbox_height, _, c, _, _ = map(float, box.split(','))
        
        xmin = int(bbox_left)
        ymin = int(bbox_top)
        xmax = int(bbox_left + bbox_width)
        ymax = int(bbox_top + bbox_height)
        
        cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,0,255), 1)
        cv2.putText(img, 
                    object_category[int(c)], 
                    (xmin, ymin - 13), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1e-3 * image_h, 
                    (0,255,0), 1)

    return img 

def drawBoundingBox_yolo(image, annotation, object_category):
    """ 

    Arg:

    Returns: 

    Example:

    """
    
    img = cv2.imread(image)
    image_h, image_w, _  = img.shape

    fl = open(annotation, 'r')
    boxes = fl.readlines()
    fl.close()

    for box in boxes:

        # Split string to float
        c, x, y, w, h = map(float, box.split(' '))

        l = int((x - w / 2) * image_w)
        r = int((x + w / 2) * image_w)
        t = int((y - h / 2) * image_h)
        b = int((y + h / 2) * image_h)

        if l < 0:
            l = 0
        if r > image_w - 1:
            r = image_w - 1
        if t < 0:
            t = 0
        if b > image_h - 1:
            b = image_h - 1

        cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)
        cv2.putText(img, 
                    object_category[int(c)], 
                    (l, t - 13), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1e-3 * image_h, 
                    (0,255,0), 1)

    return img

def test_visDroneToYolo ():
    """ 

    Arg:

    Returns: 

    Example:

    """
    
    image = "/home/max/Dropbox/Git/proyectos/UALI/ml_uali/script/VisDrone2019-DET-test-dev/images/0000006_00159_d_0000001.jpg"  
    annotation_yolo = "/home/max/Dropbox/Git/proyectos/UALI/ml_uali/script/VisDrone2019-DET-test-dev/annotations/0000006_00159_d_0000001.txt"
    annotation_visDrone ="/home/max/Dropbox/Git/proyectos/UALI/ml_uali/script/visdrone/VisDrone2019-DET-test-dev/annotations/0000006_00159_d_0000001.txt"
    
    object_category = ['ignored regions','pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor', 'others'] # visDrone - Object detection in images

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(drawBoundingBox_yolo(image, annotation_yolo, object_category))
    ax.set_title('drawBoundingBox_yolo')
    ax = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(drawBoundingBox_visDrone(image, annotation_visDrone, object_category))
    ax.set_title('drawBoundingBox_visDrone')
    plt.show()

def test_visDroneToYolo_randomPlot (path):
    """ 

    Arg:

    Returns: 

    Example:

    """
    
    images = glob.glob(path + "/*.jpg")
    random.shuffle(images)

    image_path = images[0]
    
    folder, file = os.path.split(image_path)
    annotation = file.replace(".jpg",".txt")
    anotation_path = "/home/max/Dropbox/Git/proyectos/UALI/ml_uali/script/VisDrone2019-DET-train/annotations/" + annotation
    
    object_category = ['ignored regions','pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor', 'others'] # visDrone - Object detection in images

    fig = plt.figure()
    imgplot = plt.imshow(drawBoundingBox_yolo(image_path, anotation_path, object_category))
    plt.show()

def test_richMessage ():

    message = "/home/max/Dropbox/Git/proyectos/UALI/ml_uali/script/VisDrone2019-DET-test-dev/images/0000006_00159_d_0000001.jpg"  
    Type = 'error'
    richMessage (message, Type)

if __name__ == "__main__":

    logging.basicConfig(filename='myapp.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')

    path_images = abs_path + "/VisDrone2019-DET-test-dev/images"
    path_annos = abs_path + "/VisDrone2019-DET-test-dev/annotations"
    
    #visDroneToYolo (path_images, path_annos)

    # --- TESTS ---

    test_visDroneToYolo()
    #test_visDroneToYolo_randomPlot(path_images)
    #test_richMessage ()
    #logging.info('Finished')



    

'''
VisDrone for object detection in images format 
    Format: <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
        - <bbox_left>	The x coordinate of the top-left corner of the predicted object bounding box
        - <bbox_top>	The y coordinate of the top-left corner of the predicted object bounding box
        - <bbox_width>	The width in pixels of the predicted object bounding box
        - <bbox_height>	The height in pixels of the predicted object bounding box
        - <score>	The score in the DETECTION result file indicates the confidence of the predicted bounding 
                    box enclosing an object instance.The score in GROUNDTRUTH file is set to 1 or 0. 
                    1 indicates the bounding box is considered in evaluation, while 0 indicates the bounding box will be ignored.
        - <object_category>	The object category indicates the type of annotated object, 
                    (i.e., ignored regions (0), pedestrian (1), people (2), bicycle (3), car (4), van (5), 
                    truck (6), tricycle (7), awning-tricycle (8), bus (9), motor (10), others (11))
        - <truncation>	The score in the DETECTION result file should be set to the constant -1. 
                    The score in the GROUNDTRUTH file indicates the degree of object parts appears outside a frame 
                    (i.e., no truncation = 0 (truncation ratio 0%), and partial truncation = 1(truncation ratio 1% ∼ 50%)).
        - <occlusion>	The score in the DETECTION result file should be set to the constant -1. 
                        The score in the GROUNDTRUTH file indicates the fraction of objects being occluded 
                        (i.e., no occlusion = 0 (occlusion ratio 0%), partial occlusion = 1(occlusion ratio 1% ∼ 50%), 
                        and heavy occlusion = 2 (occlusion ratio 50% ~ 100%))  
    e.g: 685,463,110,65,1,4,0,0

Yolo Darknet format
    Format:  <object_category> <bbox_left> <bbox_top> <bbox_width> <bbox_height>
    e.g: 0 0.6137131875 0.502305 0.772029 0.376537
'''

import numpy as np
import glob
import cv2
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

abs_path = os.path.dirname(os.path.abspath(__file__))

def getImageDim (path):
    """
    """
    
    images_paths = sorted(glob.glob(path + "/*.jpg"))
    imagesDim = []
    for img in tqdm(images_paths, desc="Getting image dimensions"):
        images = cv2.imread(img)
        imagesDim.append ((images.shape[1],images.shape[0]))

    return np.array(imagesDim) 

def getAnnotations(path):
    """
    """  

    paths_annos = sorted(glob.glob(path+ "/*.txt"))

    anno_list = []
    for anno_file in paths_annos:
        anno_list.append(np.loadtxt(anno_file, dtype=np.float32, delimiter=",", usecols=(5,0,1,2,3)))
    return np.array(anno_list), paths_annos

def visDroneToYolo (path_images, path_annos):
    """
    """

    imagesDim = getImageDim (path_images)
    annos, paths_annos = getAnnotations(path_annos)

    for i in tqdm(range(len(annos)), desc="Converting valid annotations"):
        for j in range(len(annos[i])):
            try:
                annos[i][j][1] = annos[i][j][1] + annos[i][j][3]/2
                annos[i][j][2] = annos[i][j][2] + annos[i][j][4]/2
                annos[i][j][1] /= imagesDim[i][0]
                annos[i][j][2] /= imagesDim[i][1]
                annos[i][j][3] /= imagesDim[i][0]
                annos[i][j][4] /= imagesDim[i][1]
            except:
                continue

    for i, path_annos in tqdm(enumerate(paths_annos), desc="Save new annotations"):
        np.savetxt(path_annos, annos[i], delimiter=" ", fmt='%f')

def drawBoundingBox_visDrone(image, annotation, object_category):
    
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

if __name__ == "__main__":

    path_images = abs_path + "/VisDrone2019-DET-test-dev/images"
    path_annos = abs_path + "/VisDrone2019-DET-test-dev/annotations"
    
    #visDroneToYolo (path_images, path_annos)

    test_visDroneToYolo()


    
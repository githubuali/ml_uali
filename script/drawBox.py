import cv2

def draw_boxes(image, boxes, labels):
    image_h, image_w, _ = image.shape
 
    for box in boxes:
        xmin = int(box.xmin*image_w)
        ymin = int(box.ymin*image_h)
        xmax = int(box.xmax*image_w)
        ymax = int(box.ymax*image_h)
 
        cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (0,255,0), 3)
        cv2.putText(image, 
                    labels[box.get_label()] + ' ' + str(box.get_score()), 
                    (xmin, ymin - 13), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1e-3 * image_h, 
                    (0,255,0), 2)
        
    return image 

# https://github.com/jbagnato/machine-learning/blob/master/Ejercicio_Object_Detection.ipynb
# https://towardsdatascience.com/how-to-use-matplotlib-for-plotting-samples-from-an-object-detection-dataset-5877fe76496d
# https://www.programiz.com/python-programming/json
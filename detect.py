import cv2
import numpy as np

def detect(especificacion,implementacion):
    i1 = cv2.imread(especificacion)
    i2 = cv2.imread(implementacion)

    size = i1.shape
    # print("asss",   size)

    i1 = cv2.resize(i1, (400,400))
    i2 = cv2.resize(i2, (400,400))

    alpha = 0.7
    blend = np.array(alpha*i1 + (1-alpha)*i2,dtype=np.uint8)


    i = cv2.cvtColor( i2-i1 , cv2.COLOR_BGR2GRAY)
    b = np.array( np.where( i==0 , 255 , 0   ) , dtype=np.uint8)

    
    blend = cv2.resize(blend, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    i = cv2.resize(i, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    b = cv2.resize(b, (size[1], size[0]) , interpolation=cv2.INTER_AREA)

    cv2.imwrite("static/imgs/blend.jpg",blend)
    cv2.imwrite("static/imgs/i.jpg",i)
    cv2.imwrite("static/imgs/b.jpg",b)


    i1_g = cv2.cvtColor( i1 , cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(i1_g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.adaptiveThreshold(i1_g,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    cv2.imwrite("static/imgs/thresh.jpg",thresh)

    contours,hierarchy = cv2.findContours(thresh, 1, 2)

    x,y,w,h = cv2.boundingRect(contours[0])
    i1_copy = i1.copy()
    cajas = []
    id = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)

        if w>20 or h>20:
            cajas.append( [id,x,y,w,h] )

            crop_img = i1[y:y+h, x:x+w]
            id+=1

            cv2.imwrite("static/imgs/res/"+str(id)+".jpg",crop_img)
            cv2.rectangle(i1_copy,(x,y),(x+w,y+h),(0,255,0),2)

    i1 = cv2.resize(i1, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    
    # cv2.imshow("bound",i1)
    cv2.imwrite("static/imgs/defectos.jpg",i1_copy)

    return cajas
    
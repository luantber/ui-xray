import cv2
import numpy as np
from sklearn.cluster import KMeans

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
            cv2.rectangle(i1_copy,(x,y),(x+w,y+h),(0,255,0),1)

    i1 = cv2.resize(i1, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    
    # cv2.imshow("bound",i1)
    cv2.imwrite("static/imgs/defectos.jpg",i1_copy)

    return cajas

def low_level(especificacion,implementacion,nombre):
    spec = cv2.imread(especificacion)
    impl = cv2.imread(implementacion)

    cv2.imwrite("static/imgs/"+ nombre +"/spec.jpg",spec)
    cv2.imwrite("static/imgs/"+ nombre +"/impl.jpg",impl)

    size = spec.shape
    # print("asss",   size)

    spec = cv2.resize(spec, (400,400))
    impl = cv2.resize(impl, (400,400))

    alpha = 0.7
    blend = np.array(alpha*spec + (1-alpha)*impl,dtype=np.uint8)

    diferencia_gris = cv2.cvtColor( spec-impl , cv2.COLOR_BGR2GRAY)
    
    #usando umbral
    diferencia_total = np.array( np.where( diferencia_gris<=10 , 255 , 0 ) , dtype=np.uint8)

    
    blend = cv2.resize(blend, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    diferencia_gris = cv2.resize(diferencia_gris, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    diferencia_total = cv2.resize(diferencia_total, (size[1], size[0]) , interpolation=cv2.INTER_AREA)

    cv2.imwrite("static/imgs/"+ nombre +"/blend.jpg",blend)
    cv2.imwrite("static/imgs/"+ nombre + "/diferencia_gris.jpg",diferencia_gris)
    cv2.imwrite("static/imgs/"+ nombre  +"/diferencia_total.jpg",diferencia_total)
    return "fin"
   
def get_boxes(imagen,nombre,spec_impl):
    i1 = cv2.imread(imagen)
       
    size = i1.shape
    i1_g = cv2.cvtColor( i1 , cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(i1_g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.adaptiveThreshold(i1_g,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

    kernel = np.ones((3,3),np.uint8)
    thresh = cv2.erode(thresh,kernel,iterations = 4)

    cv2.imwrite("static/imgs/" + nombre + "/" + spec_impl + "_thresh.jpg",thresh)

    contours,hierarchy = cv2.findContours(thresh, 1, 2)

    x,y,w,h = cv2.boundingRect(contours[0])
    i1_copy = i1.copy()
    cajas = []
    id = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)

        if w>30 and h>25:
            

            crop_img = i1[y:y+h, x:x+w]
            
            ## k means



            km = KMeans(n_clusters=2)
            crop_r = crop_img.reshape( (-1,3))
            # print(i1_r)
            km.fit(crop_r)

            # print(km.cluster_centers_)
            # print(km.labels_)

            ## 
            cajas.append( [id,x,y,w,h,km.cluster_centers_[0],km.cluster_centers_[1]] )


            cv2.imwrite("static/imgs/"+nombre+"/"+ spec_impl +str(id)+".jpg",crop_img)
            cv2.rectangle(i1_copy,(x,y),(x+w,y+h),(0,255,0),2)
            id+=1

    # i1 = cv2.resize(i1, (size[1], size[0]) , interpolation=cv2.INTER_AREA)
    
    # cv2.imshow("bound",i1)
    cv2.imwrite("static/imgs/" + nombre+"/" + spec_impl + "_cajas.jpg",i1_copy)

    return cajas

    
    
    
    
 
    
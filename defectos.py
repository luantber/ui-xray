from detect import low_level,get_boxes
import os

def intersection(a,b):
    x = max(a[0+1], b[0+1])
    y = max(a[1+1], b[1+1])
    w = min(a[0+1]+a[2+1], b[0+1]+b[2+1]) - x
    h = min(a[1+1]+a[3+1], b[1+1]+b[3+1]) - y
    if w<0 or h<0: return 0 
    return w*h

def union(a,b):
    area1 = a[3]*a[4]
    area2 = b[3]*a[4]
    return area1 + area2 - intersection(a,b)

def get_objetos(impl,spec,folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    low_level(impl,spec,folder)

    cajas_impl = get_boxes(impl,folder,"impl")
    cajas_spec = get_boxes(spec,folder,"spec")

    # print(cajas_impl)
    # print("\n")
    # print(cajas_spec)

    pares = {}
    for ci in cajas_impl:
        pares[ci[0]] = (-1,-1)
        for cs in cajas_spec:

            if intersection(ci,cs) < ci[3]*ci[4]:
                
                print("int" , intersection(ci,cs), "uni", union(ci,cs)) 
                psm = intersection(ci,cs)/union(ci,cs)        
                print(psm)
                print()
                if psm > pares[ci[0]][0] and  not psm >= 1.0 :
                    pares[ci[0]] = ( psm , cs[0] )

    return pares,cajas_impl,cajas_spec #impl_0 ---> ( 3.009 , spec_4 )  

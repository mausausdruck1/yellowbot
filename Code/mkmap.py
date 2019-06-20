# map
import math
import numpy as np
import config as cf
#import drivecntrl as dc

map=[0,0,0,0]#y,x winkel rad global, winkel rad rel.
waylog=[[0,0,0]]#list y,x, winkel in °
debug=1
def update(way):
    global map, waylog
    mean=np.mean(way)*cf.waymulti
    delta=(way[0]-way[1])*cf.waymulti
    a=map[2];
    if delta>20:
        delta=20;
    if delta <-20:
        delta=-20
    alpha=math.asin(delta/20)
    
    y=math.cos(alpha+a)*mean
    x=math.sin(alpha+a)*mean
    y=round(y,2)
    x=round(x,2)
    if x>= 0.1 or y>=0.1:
        waylog.append([round(map[0]+y),round(map[1]+x), round(math.degrees(alpha+a))])
        map=[map[0]+y,map[1]+x,map[2]+round(alpha,6),round(alpha,6)]

def reset():
    global map,waylog
    waylog=[[0,0,0]]
    map=[0,0,0,0]
    print('map reset!')

    
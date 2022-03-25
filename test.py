


import os
import numpy as np
from numpy import *
from time import *
from PIL import Image


def rename(path_0):
    print('start')    
    folderlist=os.listdir(path_0)
    for folder in folderlist:
        inner_path = os.path.join(path_0, folder)    
        total_num_folder = len(folderlist)       #文件夹的总数    
        filelist = os.listdir(inner_path)
    
        i=0
        for item in filelist:
            total_num_file=len(filelist)
            if item.endswith('.raw'):
                time1=time()
                src=os.path.join(os.path.abspath(inner_path),item)
                dst=os.path.join(path_0,str(folder)+'_'+'frame100'+'_'+str(i)+'.yuv')
                try:
                    os.rename(src, dst)
                    i += 1
                except:
                    continue

                ###格式转换并另存###
                bgr=yuv2rgb(dst)
                t=Image.fromarray(bgr)
                t.save(os.path.join(path_0,str(folder)+'_'+'frame100'+'_'+str(i)+'.bmp')) 
                time2=time()               
                print(str(folder)+'_'+str(i)+': done 耗时：%ds' % int(time2-time1) )   
    print('all fodler done,number is: %d' % total_num_folder,'\n','end')

def yuv2rgb(path_0):

    ###提取y、u、v数据###
    y=np.zeros((2160*3840),np.uint8)
    u=np.zeros((1080*3840),np.uint8)
    v=np.zeros((1080*3840),np.uint8)
    with open(path_0,'rb') as reader:
        for i in range(1080*3840):
            u[i]=ord(reader.read(1))
            y[2*i]=ord(reader.read(1))
            v[i]=ord(reader.read(1))
            y[2*i+1]=ord(reader.read(1))   
    y=y.reshape(2160,3840)
    u=u.reshape(2160,1920)
    v=v.reshape(2160,1920)
    ###yuv转bgr(bmp)###
    bgr_data = np.zeros((2160, 3840, 3), dtype=np.uint8)
    V = np.repeat(v, 2, 1)
    U = np.repeat(u, 2, 1)
    
    c = (y-np.array([16])) * 298
    d = U - np.array([128])
    e = V - np.array([128])
    
    r = (c + 409 * e + 128) // 256
    g = (c - 100 * d - 208 * e + 128) // 256
    b = (c + 516 * d + 128) // 256

    r = np.where(r < 0, 0, r)
    r = np.where(r > 255,255,r)

    g = np.where(g < 0, 0, g)
    g = np.where(g > 255,255,g)

    b = np.where(b < 0, 0, b)
    b = np.where(b > 255,255,b)

    bgr_data[:, :, 2] = b
    bgr_data[:, :, 1] = g
    bgr_data[:, :, 0] = r

    return bgr_data

def raw2rggb(path,row,col):
    data=np.fromfile(path,np.uint16)
    x=data.copy()
    x=x.reshape(row,col)//16
    x=np.where(x<0,0,x)
    x=np.where(x>255,255,x) 
    #print(data.shape,np.max(data))
    
    rggb=np.zeros((row,col,3),dtype=np.uint8)
    for i in range(0,row,2):
        for j in range(0,col,2):
            rggb[i,j,0]=x[i,j]
            rggb[i,j+1,1]=x[i,j+1]
            rggb[i+1,j,1]=x[i+1,j]
            rggb[i+1,j+1,2]=x[i+1,j+1]
    return rggb


if __name__ == '__main__':

    start_time=time()

    path_0='E:\\0307\\' #所有子文件夹的目录
    rename(path_0)

    end_time=time()
    print('程序运行时间：%d秒' % int(end_time-start_time))

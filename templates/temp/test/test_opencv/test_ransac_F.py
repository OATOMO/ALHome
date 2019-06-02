#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 16:28'
__author__ = 'Colby' 
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

def findF_8_point():
    p1 = np.array([[0.180123, -0.156584], [0.291429, 0.137662], [-0.170373, 0.0779329], [0.235952, -0.164956],
                   [0.142122, -0.216048], [-0.463158, -0.132632], [0.0801864, 0.0236417], [-0.179068, 0.0837119]])
    p2 = np.array([[0.208264, -0.035405], [0.314848, 0.267849], [-0.144499, 0.190208], [0.264461, -0.0404422],
                   [0.171033, -0.0961747], [-0.427861, 0.00896567], [0.105406, 0.140966], [-0.15257, 0.19645]])
    Fretval, mask = cv.findFundamentalMat(p1, p2, method=cv.FM_8POINT)
    print(p1.shape)
    print('F Matrix SVD ')
    w, u, v = cv.SVDecomp(Fretval)
    print(w)


def findF_RANSAC():
    file = open("correspondences.txt") #打开存放点坐标的文件
    p1 = np.zeros((274,2))
    p2 = np.zeros((274,2))
    i = 0
    for line in file:   #读取坐标文件
        point_list = line.split()
        if len(point_list) == 4:
            p1[i,0] = float(point_list[0])
            p1[i,1] = float(point_list[1])
            p2[i,0] = float(point_list[2])
            p2[i,1] = float(point_list[3])
            i+=1

    file.close()
    myThreshold = 0.0015*0.0015
    Fretval, mask = cv.findFundamentalMat(p1, p2, method=cv.FM_RANSAC,
                                         ransacReprojThreshold=myThreshold,confidence=0.99)
    print( '保留点数 ： '+str( cv.countNonZero(mask)))
    print('F Matrix is -> :')
    print(Fretval)
    print('F Matrix SVD ')
    w,u,v = cv.SVDecomp(Fretval)
    print(w)



def main():
    findF_8_point()
    # findF_RANSAC()

if __name__ == '__main__':
    main()



#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 14:49'
__author__ = 'Colby'

import matplotlib.pyplot as plt
import numpy as np
#三个点的坐标
x = [2, 4, 6]
y = [2, 4, 5]
plt.xlim(0, 7)  #坐标轴长度设置
plt.ylim(0, 7)
plt.scatter(x,y)#散点
#   c+xd=y
#   c+2d=2
#   c+4d=4
#   c+6d=5
A = np.matrix([[1,x[0]],
               [1,x[1]],
               [1,x[2]]])

b = np.array([y[0],y[1],y[2]])
#求出直线拟合的最优解
x_ = np.dot(np.dot(np.dot(A.T,A).I,A.T),b)
c = x_[0,0]
d = x_[0,1]
#生成直线
dx = np.arange(1,10)
dy = c+d*dx
plt.plot(dx,dy) #画出直线
plt.xlabel('x')
plt.ylabel('y')
plt.title('LS')
plt.show()
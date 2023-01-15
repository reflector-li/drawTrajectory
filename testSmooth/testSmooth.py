# coding: utf-8

'''
@File: testSmooth.py 
@Date: 2022/4/12
'''

import numpy as np
import matplotlib.pyplot as plt

optimalWaypoints = np.loadtxt("optimalWaypoints.txt")
resampleWaypoints = np.loadtxt("resampleWaypoints.txt")

plt.subplot(1,2,1)
plt.plot(range(optimalWaypoints.shape[0]),optimalWaypoints[:,2],'.',color='blue')
plt.title("plot1")
#

plt.subplot(1,2,2)
plt.plot(range(resampleWaypoints.shape[0]),resampleWaypoints[:,2],'.',color = 'red')
plt.title("plot2")


plt.show()



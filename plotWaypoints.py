# coding: utf-8

'''
@File: plotWaypoints.py 
@Date: 2022/3/24
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


arrayWithVec = True

if arrayWithVec:
    wayPoints = np.loadtxt("./data/path1.txt")
    originalWaypoints = np.loadtxt("./data/resampleWaypoints.txt")
    #plt.quiver(wayPoints[:,0],wayPoints[:,1],np.cos(wayPoints[:,2]),np.sin(wayPoints[:,2]),1)
    plt.plot(wayPoints[:,0],wayPoints[:,1],color='blue')
    # plt.plot(originalWaypoints[:, 0], originalWaypoints[:, 1],color='red')

    plt.show()

else:
    optimalWaypoints = np.loadtxt("./data/waypoints.txt")
    originalWaypoints = np.loadtxt("./data/obstacles.txt")

    plt.plot(optimalWaypoints[:,0],optimalWaypoints[:,1],'-',color='blue')
    plt.plot(originalWaypoints[:,0],originalWaypoints[:,1],'.',color='red')
    plt.plot(55.0000,460.0000,'.',color = 'green')
    plt.xlim(originalWaypoints[0, 0] - 20, originalWaypoints[0, 0] + 50);
    plt.ylim(originalWaypoints[0, 1] - 30, originalWaypoints[0, 1] + 50);
    #plt.plot([originalWaypoints[15,0],originalWaypoints[17,0]],[originalWaypoints[15,1],originalWaypoints[17,1]],'.',color = 'blue')
    #plt.plot([373.9,409.8], [572.9,608.1],'.', color='blue')
    plt.show()


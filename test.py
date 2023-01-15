import numpy as np
import matplotlib.pyplot as plt
# #
# # originalWaypoints = np.loadtxt("./data/waypoints.txt")
# # total = 0
# # for i in range(originalWaypoints.shape[0]-1):
# #      length = np.sqrt(np.power((originalWaypoints[i+1,0] - originalWaypoints[i,0]),2)+np.power((originalWaypoints[i+1,1] - originalWaypoints[i,1]),2))
# #      total = length+total
# #
# # print(total)
#
# coeff1 = np.array([11.686,0,0,-0.0768661,0.0115299,-0.000464497])
# coeff2 = np.array([97,-36,5.4,-0.39,0.0135,-0.00018])
# s1 = range(0,10)
# s2 = range(10,20)
# l1 = np.zeros(10)
# l2 = np.zeros(10)
# count = 0
# for i in s1:
#      l_ = coeff1[0] + coeff1[1] * i + coeff1[2] * i ** 2 + coeff1[3] * i ** 3 + coeff1[4] * i ** 4 + coeff1[5] * i ** 5
#      l1[count] = l_
#      count = count+1
#
# count = 0
# for i in s2:
#      l_ = coeff2[0] + coeff2[1] * i + coeff2[2] * i ** 2 + coeff2[3] * i ** 3 + coeff2[4] * i ** 4 + coeff2[5] * i ** 5
#      l2[count] = l_
#      count = count + 1
# print(l2)
# plt.plot(s1,l1,'.r')
# plt.plot(s2,l2,'.b')
# plt.show()

low = np.loadtxt("./data/lowerBound.txt")
upper = np.loadtxt("./data/upperBound.txt")
s = range(0,60)
plt.plot(s,low,'.r')
plt.plot(s,upper,'.b')
plt.plot([14.5452 ,24.5599 ,32.3613 ],[0.0423308,-0.130141,0.0949282],'.c')
plt.show()
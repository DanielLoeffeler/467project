import numpy as np

a = np.array([[0,3,8,0,2,1],[1,3,10,0,1,1],[2,1,14,0,1,1]])

def sortit(a):
    i=0
    order = 1
    x = a.shape[0]
    while order==1:
        order=0
        for i in range(x-1):
            if (a[i,2] <= a[i+1,2]) and (a[i,3] == -1) and (a[i+1,3]!=-1):
                a[[i, i + 1]] = a[[i + 1, i]]
                order=1
            elif (a[i, 2] > a[i + 1, 2]) and (a[i + 1, 3] == -1) and (a[i,3]==-1):
                a[[i, i + 1]] = a[[i + 1, i]]
                order = 1
            elif (a[i,2]>a[i+1,2]) and (a[i+1,3]!=-1):
                a[[i,i+1]]=a[[i+1,i]]
                order=1


    return a
print(sortit(a) )
"""
This code runs the math behind the system

-1 = tasks not schedulable
"""
import numpy as np

a = np.array([[0,5,15,5,2],[1,5,10,5,1],[2,1,12,1,1],[3,2,6,1,1]])

def sortitmotherfucker(a):
    i=0
    order = 1
    x = a.shape[0]
    while order==1:
        order=0
        for i in range(x-1):
            if a[i,2]>a[i+1,2]:
                a[[i,i+1]]=a[[i+1,i]]
                order=1
    return a


def frequencyCalc(a):
    sortitmotherfucker(a)
    i=0
    x = a.shape[0]
    y = a.shape[1] - 3
    Release=np.zeros(x)
    for i in range(x):
        Release[i]=a[i,2]
    print(a)
    print(Release)
    Freq=0
    output=np.zeros((x*y,4))
    index=0
    R=0
    T=np.amax(Release)*y
    T=int(T)
    print(T)
    for t in range(T):
        Freq=0
        minR=int(np.amin(Release))
        if index == 0:
            for r in range(x):
                Freq = Freq + a[r, 1] / a[r, 2]
            if Freq > 1:
                return -1
            else:
                output[index, 2] = Freq

                output[index, 0] = 0
                output[index, 1] = a[0, 3] * Freq
                output[index, 3] = a[0, 0]
                index += 1
                Release[a[0,0]]=2*a[0,2]
                R+=1
        elif index < x:
            for r in range(x):
                if R > r:
                    Freq = Freq + a[r, 3] / a[r, 2]
                else:
                    Freq = Freq + a[r, 1] / a[r, 2]
            output[index, 2] = Freq
            output[index, 0] = output[index - 1, 1]
            output[index, 1] = output[index, 0] + a[R, 3] * Freq
            output[index, 3] = a[R, 0]
            R += 1
            index += 1



    """for I in range(y):
        z=I+3
        R=0
        for i in range(x):
            Freq=0
            if task == 0:
                for r in range(x):
                    Freq = Freq + a[r,1] / a[r,2]
                if Freq > 1:
                    return -1
                else:
                    output[task,2]=Freq

                    output[task,0]=0
                    output[task,1]=a[i,z]*Freq
                    output[task,3]=a[i,0]
                    task+=1
                    R+=1

            else:
                for r in range(x):
                    if R>r:
                        Freq = Freq + a[r, z] / a[r, 2]
                    else:
                        Freq = Freq + a[r, 1] / a[r, 2]

                output[task,2]=Freq
                output[task,0]=output[task-1,1]
                output[task,1]=output[task,0]+a[i,z]*Freq
                output[task,3]=a[i,0]
                R+=1
                task+=1
"""


    return output




print(frequencyCalc(a))

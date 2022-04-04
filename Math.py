"""
This code runs the math behind the system

-1 = tasks not schedulable
"""
import numpy as np

a = np.array([[0,3,8,2,1],[1,3,10,1,1],[2,1,14,1,1]])

def sortitmotherfucker(a):
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

def findnext(a,Release,x):
    for i in range(x):
        if (Release[0,0]==a[i,0]) and (Release[0,3]!=-1):
            return i
    exit(-99)


def GetValues(a,Release,x,y):
    Value=np.zeros((x,2))

    for r in range(x):
        for i in range(x):
            if a[i,0]==Release[r,0]:
                Value[r,1]=a[i,2]
                # If released
                if Release[r,3]==0:
                    Value[r,0]=a[i,1]
                elif Release[r,3]==-1 and Release[r,1]!=-1:
                    temp=int(Release[r,1]+2)
                    Value[r,0]=a[i,temp]
                else:
                    Value[r,0]=a[i,y+2]
    return Value


def calculateFrequency(a,Release,x,y,b):
    Values=GetValues(a,Release,x,y)
    print(Values)
    Freq=0
    for r in range(x):
        Freq = Freq + Values[r, 0] / Values[r, 1]
    return Freq

def CheckNextRelease(Release,TF,x):
    for i in range(x):
        if Release[i,3]==-1:
            if TF <= Release[i,2]:
                return TF
            else:
                t=Release[i,2]
                return t

def assignoutput(a,b,output,Freq,TF,index):
    output[index, 2] = Freq

    output[index, 0] = output[index-1,1]
    output[index, 1] = TF
    if b!=-1:
        output[index, 3] = a[b, 0]
    else:
        output[index,3] = -1
    return output

def ReleaseNext(Release,x):
    for i in range(x):
        if Release[i,3]==-1:
            Release[i,3]=0
            return Release

def checkfinished(Release,x,y):
    for i in range(x):
        if Release[i,1]!=y:
            return 1
    return 0

def checkRelease(Release,x):
    for i in range(x):
        if Release[i,3]!=-1:
            return 0
    return 1

def Run(a):
    #Initial sorting function to sort earliest deadline first
    a=sortitmotherfucker(a)
    i=0
    x = a.shape[0]
    y = a.shape[1] - 3
    Release=np.zeros((x,5))
    for i in range(x):
        Release[i,2]=a[i,2]
        Release[i,0]=a[i,0]
    print(a)
    print(Release)

    output=np.zeros((x*y*2+3,4))
    index=0
    R=0
    finish=0
    Freq=0
    for r in range(x):
        Freq = Freq + a[r, 1] / a[r, 2]
    if Freq > 1:
        return -1
    else:
        output[index, 2] = Freq

        output[index, 0] = 0
        output[index, 1] = a[0, 3] / Freq
        output[index, 3] = a[0, 0]
        index += 1
        Release[0,1]+=1
        Release[0, 3] = -1

        if Release[0,1]>y:
            Release[0,2]=-1
        Release=sortitmotherfucker(Release)




    # Sort Release to put earliest deadline first that has released
    Release = sortitmotherfucker(Release)
    print(Release)
    #check if we have anything to run
    while checkfinished(Release,x,y):
        if checkRelease(Release,x):
            # Ensure earliest deadline task is next to run.
            sortitmotherfucker(Release)
            # Set end time equal to start of next release
            TF=Release[0,2]

            # As no task should be running set task to -1
            b=-1

            # Calculate the Waiting Frequency cause we can
            Freq=calculateFrequency(a,Release,x,y,b)

            # Update the output to reflect that we are waiting
            output=assignoutput(a,b,output,Freq,TF,index)

            # Increment index to reflect the change in state
            index+=1

            # Since we have hit a release, release the next task
            Release=ReleaseNext(Release,x)

        else:
            # Ensure first task is next task to run
            sortitmotherfucker(Release)

            # Find associate row of a to first row of Release
            b=findnext(a,Release,x)

            # Calculate the Frequency based on current system state
            Freq=calculateFrequency(a,Release,x,y,b)

            #Prepare to run next iteration
            c= int(Release[0,1])+3

            #Calculate the time the task will finish
            TF=a[b,c]/Freq + output[index-1,1]

            #Save the time temporarily
            temp=TF

            #Check if the task will finish before the next task releases
            TF=CheckNextRelease(Release,TF,x)

            #update output regardless of task finishing successfully or not
            output = assignoutput(a, b, output, Freq, TF, index)

            # Increment index to reflect the change in state
            index += 1

            #if there was no change in final time task completed successfully therefore Release must be updated accordingly
            if TF==temp:
                # Increment to show that previous Invocation was run successfuly
                Release[0,1]+=1

                #Set the flag to show task has run to completion
                Release[0, 3] = -1
                # Update task deadline
                Release[0, 2] = a[b, 2] * (Release[0, 1] + 1)
                # Check if that was the last iteration to run
                if Release[0,1]>=y:
                    Release[0,2]=np.max(Release)*(y+1)+1
            # For when they did not match up
            else:

    return output

"""
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
        Release[a[0, 0]] = 2 * a[0, 2]
        R += 1
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

    for I in range(y):
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



print(Run(a))

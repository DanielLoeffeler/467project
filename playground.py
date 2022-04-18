import numpy as np
import matplotlib.pyplot as plt

# [[label1, worstcom1, period1,Release, invocations1, invocation2, invocation3];
# [[label1, worstcom1, period1, invocations1, invocation2, invocation3];
#  [label2, worstcom2, period2, invocations2]]
# [[frequencies]]

# [[label1, calculated1];
#  [label2, calculated2]]
# where calculated:
# [[start,stop,frequency], [start,stop,frequency], [start,stop,frequency]]

"""
make an x linspace from 0 to the end of the last task with a certain resolution
make arrays with of the length of that x array filled with 0, then 
for the ranges where a task is (between start and stop) , fill that range with the frequency value
"""


def change_range(arr, start, stop, val):
	# Change values in the numpy array in arr in the range of start and stop with val
	rang = np.arange(round(start), round(stop), 1, dtype=int)

	for x in rang:
		arr[x] = val
	return arr


def make_yval(ranges, res, xrange):
	# Takes the instance array and returns the array containing the values for each instance of time
	taskval = np.zeros(xrange.size)

	for i, item in enumerate(ranges):
		taskval = change_range(taskval, item[0] / res, item[1] / res, item[2])

	return taskval


# taskval = np.zeros(xrng.size)
#
# for i, item in enumerate(task1):
# 	taskval = change_range(taskval, item[0]/resolution, item[1]/resolution, item[2])
# 	print(taskval)

# item = np.array([0, 2.3, 1])
# test = np.arange(0, 30, 1)
# test = change_range(test, item[0]/resolution, item[1]/resolution, 4)


# yval1 = [0, 1, 1, 0, 0, 0, 0, .5, .5, .5, .5, 0, 0, 0, 0, 0, 1, 1, 1, 1]
# yval2 = [0, 0, 0, .5, .5, .5, .5, 0, 0, 0, 0, 0, .25, .25, .25, .25, 0, 0, 0, 0]

resolution = 0.01
lastpoint = 20
xrng = np.arange(0, lastpoint, resolution)

task1 = np.array([[0, 2.3, 1], [4.5, 6, 0.25], [13, 16, 0.5]])
task2 = np.array([[2.3, 4, 0.5], [7, 10, 0.75], [11, 12, 1], [16, 19, 0.25]])

yval1 = make_yval(task1, resolution, xrng)
yval2 = make_yval(task2, resolution, xrng)

ax1 = plt.subplot()
ax1.set_xticks([0, 2.3, 4, 4.5, 6, 7, 10, 11, 12, 13, 16, 19])
ax1.set_yticks([0, .25, .5, .75, 1])

plt.bar(xrng, yval1, width=resolution, align="center", color='red')
plt.bar(xrng, yval2, width=resolution, align="center", color='blue')

plt.show()

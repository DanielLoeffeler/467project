import numpy as np
import matplotlib.pyplot as plt
import Math as EDF
from math import ceil

# [[label1, worstcom1, period1, release1, invocations1,1, invocations1,2],
#  [label2, worstcom2, period2, release2, invocations2,1, invocations2,2]]
# [[frequencies]]

# [[label1, instances1]
#  [label2, instances2]]
# where instances:
# [[start,stop,frequency], [start,stop,frequency], [start,stop,frequency]]

"""
make an x linspace from 0 to the end of the last task with a certain resolution
make arrays with of the length of that x array filled with 0, then
for the ranges where a task is (between start and stop) , fill that range with the frequency value
"""





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



def dopl(given, calculated, resolution, endpoint, ltn, lk):
    def make_yval(ranges, res, xrange):
        # Takes the instance array and returns an array containing the frequency values for each unit of time
        # between the start and the stop
        taskval = np.zeros(xrange.size)
        # print(ranges)
        for i, item in enumerate(ranges):
            if item[2] == -1:
                # taskval[int(item[0] // res):int(item[1] // res)] = 0
                taskval[int(item[1] // res)-10:int(item[1] // res)] = 1.25
            else:
                taskval[int(item[0] // res):int(item[1] // res)] = item[2]
            # print(int(item[0] // res))
        return taskval

    # Makes all the poitn on x axis for data
    xrng = np.arange(0, endpoint, resolution)

    # Take calculated result and break it into one 3D array where each array one step in is all one task
    hold=np.zeros((given.shape[0],calculated.shape[0],3))

    for taskamt in range(given.shape[0]):
        # for invocamt in range(given.shape[1]-3):
        for index, x in enumerate(calculated[calculated[:, -1] == taskamt]):
            hold[taskamt, index]=x[0:3]

    colourlist=['b','g','r','c','m','y','k','w']
    yvals=[]

    ax1 = plt.subplot()
    print (calculated)
    # extract all the xticks from calculated array
    xticks=[]
    for item in calculated:
        for x in range(2):
            # print(item[x])
            xticks.append(item[x])

    ax1.set_xticks(xticks, rotation=45)

    # extracts all the yticks (freq value) from calculated array
    yticks=[]
    for item in calculated:
        yticks.append(round(item[2],2))

    # yticks = [round(num, 2) for num in yticks]
    ax1.set_yticks(yticks)

    # Add each task array to the plot with a unique colour
    for index, tasklist in enumerate(hold):
        yvals=make_yval(tasklist, resolution, xrng)
        plt.bar(xrng, yvals, width=resolution, align="center", color=colourlist[index])

    # plot the label text above the center of the invocation with the str being the freq value or "over" if overrun
    print(calculated)
    for index, item in enumerate(calculated):
        if item[0] == item[1]:
            xpos = -10
        else:
            xpos = (int(item[0]) + int(item[1])) / 2

        if item[2] == -1:
            plt.text(item[1], 1.25, 'overrun', ha='center')
        else:
            plt.text(xpos, item[2], str(round(item[2],2)), ha='center')

    names=[]
    for index, x in enumerate(given):
        names.append(str(ltn[lk[index]]))  # Replaces each label assigned number with its label

    plt.legend(names, loc='upper right')
    plt.xticks(rotation=90)
    plt.show()

def runprog(givene, z, ltn, lk):
    calculatede = EDF.Run(givene,z )

    # Remove all rows with only zeroes in them
    calculatede = calculatede[~np.all(calculatede == 0, axis=1)]

    # Remove all rows where the last item is -1
    calculatede = calculatede[calculatede[:, -1] != -1]

    resolutione = 0.01

    endpointe = ceil(calculatede[-1,-3])+1

    dopl(givene, calculatede, resolutione, endpointe, ltn, lk)


# given = np.array([[0, 3, 8, 2, 2, 1],
#                   [1, 3, 10, 0, 1, 1],
#                   [2, 1, 14, 0, 1, 1]])
given = np.array([[0,9,8,0,9,1],[1,3,10,0,1,1],[2,1,14,0,1,1]])

labeltonumber = {0: 'a', 1: 'b', 2: 'c'}
labelkeys = range(0, 3)
z=0
runprog(given, z, labeltonumber, labelkeys)



# print(hold)
# tasks = np.array([[0, 2.3, 1, 0],
#                   [2.3, 4, 0.5, 1],
#                   [4.5, 6, 0.25, 0],
#                   [7, 10, 0.75, 1],
#                   [11, 12, 1, 1],
#                   [13, 16, 0.5, 0],
#                   [16, 19, 0.25, 1]])
#
#
# calculated = calculated[calculated[:,-1] !=-1]
#
# print(n)
# yval1=make_yval(calculated, resolution, xrng)
# print(yval1)
# task1 = np.array([[0, 2.3, 1], [4.5, 6, 0.25], [13, 16, 0.5]])
# task2 = np.array([[2.3, 4, 0.5], [7, 10, 0.75], [11, 12, 1], [16, 19, 0.25]])
#
# yval1 = make_yval(task1, resolution, xrng)
# yval2 = make_yval(task2, resolution, xrng)
# for t in tasks:
#     print(make_yval(t, resolution, xrng))
# ax1 = plt.subplot()
# ax1.set_xticks([0, 2.3, 4, 4.5, 6, 7, 10, 11, 12, 13, 16, 19])
# ax1.set_yticks([0, .25, .5, .75, 1])
# #
# plt.bar(xrng, yval1, width=resolution, align="center", color='red')
# plt.bar(xrng, yval2, width=resolution, align="center", color='blue')
#
# plt.show()
#
#
# given = np.array([[0, 3, 8, 2, 1], [1, 3, 10, 1, 1], [2, 1, 14, 1, 1]])
# calculated = EDF.Run(given)
#
# # Remove all rows with only zeroes in them
# calculated = calculated[~np.all(calculated==0, axis=1)]
#
# # Remove all rows where the last item is -1
# calculated = calculated[calculated[:,-1] !=-1]



# import tkinter as tk
# from tkinter import ttk
# import GUIbackend as GUI
# import re
# import numpy as np
#
# root = tk.Tk()
#
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky='nsew')
#
# treeframe = ttk.Frame(mainframe)
# treeframe.grid()
#
# columns = ['Task', 'Worst time', 'Period']
# tree = ttk.Treeview(treeframe, columns=columns, show="headings")
#
# tree.grid(column=0, row=0, sticky='new', columnspan=3)
#
# tree.column(0, stretch=True, width=100)
# tree.column(1, stretch=True, width=150)
# tree.column(2, stretch=True, width=75)
#
# tree.heading('Task', text='Task')
# tree.heading('Worst time', text='Worst Computation')
# tree.heading('Period', text='Period')
#
# Tinvoc1 = tk.StringVar()
# Tinvoc1_E = ttk.Entry(mainframe, textvariable=Tinvoc1)
# Tinvoc1_E.grid(column=0, row=1)
#
#
# def addtotree(treee, invoc, col):
# 	global columns
# 	global tree
#
# 	# Goes through invocation string list and creates list with just the numbers in that string
# 	# tempinvoc = ""
# 	# for l in invoc:
# 	# 	if l.isdigit():
# 	# 		tempinvoc = tempinvoc + "," + l
# 	# invoc = tempinvoc[1:].split(",")
# 	invoc = re.findall("[0-9]+", invoc)
#
# 	# if there are more items in the invocation list
# 	if len(invoc) > len(columns[3:]):
# 		columns = ['Task', 'Worst time', 'Period']
# 		columns.extend(list(np.arange(1, len(invoc)+1)))
# 		treeee = ttk.Treeview(treeframe, columns=columns, show="headings")
# 		treeee.column(0, stretch=True, width=100)
# 		treeee.column(1, stretch=True, width=150)
# 		treeee.column(2, stretch=True, width=75)
#
# 		treeee.heading('Task', text='Task')
# 		treeee.heading('Worst time', text='Worst Computation')
# 		treeee.heading('Period', text='Period')
#
# 		for ind, item in enumerate(columns[3:]):
# 			ind = 3+ind
# 			treeee.column(ind, stretch=True, width=100)
# 			treeee.heading(item, text='invocation '+str(ind-2))
#
# 		tree.destroy()
# 		tree = treeee
# 		tree.grid(column=0, row=0)
#
# AddTask_B = tk.Button(
# 	mainframe,
# 	text='Add Task',
# 	command=lambda: addtotree(tree, Tinvoc1.get(), columns)
# )
#
# pb = tk.Button(
# 	mainframe,
# 	text="print",
# 	command=lambda: print(columns)
# )
#
# AddTask_B.grid(column=1, row=1, sticky='ew')
# pb.grid(column=2, row = 1)
# root.mainloop()


# from tkinter import ttk
# from tkinter import *
#
# root = Tk()
# treeframe = ttk.Frame(root)
# treeframe.grid(column=0, row=0)
# columns = ("Items", "Values", "extra")
# Treeview = ttk.Treeview(treeframe, height=18, show="headings", columns=columns)  #
#
# Treeview.column("Items", width=200, anchor='center')
# Treeview.column("Values", width=200, anchor='center')
# Treeview.column("extra", width=200, anchor='center')
#
# Treeview.heading("Items", text="Items")
# Treeview.heading("Values", text="Values")
# Treeview.heading("extra", text="extra")
#
# Treeview.pack(side=LEFT, fill=BOTH)
#
# name = ['Item1', 'Item2', 'Item3']
# ipcode = ['10', '25', '163']
# for i in range(min(len(name), len(ipcode))):
#     Treeview.insert('', i, values=(name[i], ipcode[i]))
#
#
# def treeview_sort_column(tv, col, reverse):
#     l = [(tv.set(k, col), k) for k in tv.get_children('')]
#     l.sort(reverse=reverse)
#     for index, (val, k) in enumerate(l):
#         tv.move(k, '', index)
#         tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
#
#
# def set_cell_value(event):
#     try:
#         for item in Treeview.selection():
#             item_text = Treeview.item(item, "values")
#             column = Treeview.identify_column(event.x)
#             row = Treeview.identify_row(event.y)
#         cn = int(str(column).replace('#', ''))
#         rn = int(str(row).replace('I', ''))
#         print(cn,rn)
#         entryedit = Text(root, width=10 + (cn - 1) * 16, height=1)
#         entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)
#
#         def saveedit():
#             Treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
#             entryedit.destroy()
#             okb.destroy()
#
#         okb = ttk.Button(root, text='OK', width=4, command=saveedit)
#         okb.place(x=90 + (cn - 1) * 242, y=2 + rn * 20)
#     except:
#         print('not in the treeview')
#
# def newrow():
#     name.append('to be named')
#     ipcode.append('value')
#     Treeview.insert('', len(name) - 1, values=(name[len(name) - 1], ipcode[len(name) - 1]))
#     Treeview.update()
#     newb.place(x=120, y=(len(name) - 1) * 20 + 45)
#     newb.update()
#
#
# Treeview.bind('<Double-1>', set_cell_value)
#
# newb = ttk.Button(root, text='new item', width=20, command=newrow)
# newb.place(x=120, y=(len(name) - 1) * 20 + 45)
#
# for col in columns:
#     Treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(Treeview, _col, False))
#
#
# root.mainloop()


# # [[label1, instances1]
# #  [label2, instances2]]
# # where instances:
# # [[start,stop,frequency], [start,stop,frequency], [start,stop,frequency]]


# class Car():
#     """A simple attempt to represent a car."""
#     def __init__(self, make, model, year):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.odometer_reading = 0
#
#     def get_descriptive_name(self):
#         long_name = str(self.year) + ' ' + self.make + ' ' + self.model
#         return long_name.title()
#
#     def read_odometer(self):
#         print("This car has " + str(self.odometer_reading) + " miles on it.")
#
#     def update_odometer(self, mileage):
#         if mileage >= self.odometer_reading:
#             self.odometer_reading = mileage
#         else:
#             print("You can't roll back an odometer!")
#
#     def increment_odometer(self, miles):
#         self.odometer_reading += miles
#
#
# class ElectricCar(Car):
#     """represent electric car"""
#     def __init__(self, make='butt', model='poop', year=3):
#         super().__init__(make, model, year)
#
#
#
# import tkinter as tk
# from tkinter import ttk
# import numpy as np
#
#
# class Newtreeview():
#     """ttk treeview but with some more methods to control the amount of columns there are"""
#
#     def __init__(self, frame, columns, show):
#         self.frame = frame
#         self.columns = columns
#         self.show = show
#         self.tree = ttk.Treeview(frame, columns=columns, show=show)
#
#     def printcolumns(self):
#         print(self.columns)
#
#     def setinvoccol(self, invocs):
#         """Sets the amount of invocation columns to the given amount"""
#         self.columns = ['Task', 'Worst time', 'Period']
#         self.columns.extend(list(np.arange(1, invocs+1 )))
#         print(self.columns)
#         self.tree.destroy()
#         self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings")
#
#         for index, item in enumerate(self.columns):
#             self.tree.column(item, stretch=True, width=100, minwidth=100)
#             self.tree.heading(item, text=item)
#             print(index, item)
#
#         for index, item in enumerate(self.columns[3:]):
#             index = 3 + index
#             self.tree.column(index, stretch=True, width=100, minwidth=100)
#             self.tree.heading(item, text='invocation ' + str(index - 2))
#
#         self.tree.grid(column=0, row=0, sticky='new', columnspan=invocs+3)
#
#         self.tree.bind('<Double-1>', tree.set_cell_value)
#
#         filler = ['', '', '', '', '', '', '', '', '', '', '', '']
#         for i in range(min(len(filler), len(filler))):
#             tree.tree.insert('', 'end', values=(filler[i]))
#
#     def set_cell_value(self, event):
#         try:
#             # Find the column and row that is clicked on
#             for item in self.tree.selection():
#                 item_text = self.tree.item(item, "values")
#                 column = self.tree.identify_column(event.x)
#                 row = self.tree.identify_row(event.y)
#             cn = int(str(column).replace('#', ''))
#             rn = int(str(row).replace('I', ''))
#
#             # Finds the sum of pixels to the left of clicked on column
#             colwidths=0
#             for co in range(cn-1):
#                 if cn == 1:
#                     colwidths=0
#                 else:
#                     colwidths+=self.tree.column(co)['width']
#
#             # Makes an entry form at the width of the column
#             entryedit = tk.Text(self.frame, width=self.tree.column(cn-1)['width']//7, height=1, font=("consolas",10))
#             entryedit.place(x=colwidths, y=6 + rn * 20)
#
#             def saveedit():
#                 self.tree.set(item, column=column, value=entryedit.get(0.0, "end"))
#                 entryedit.destroy()
#                 okb.destroy()
#
#             # Makes the OK button to the left of rightmost edge of the clicked on column
#             okb = ttk.Button(mainframe, text='OK', width=4, command=saveedit)
#             okb.place(x=colwidths+self.tree.column(cn-1)['width'], y=2 + rn * 20)
#
#         except:
#             print('not in the treeview')
#
#
# root = tk.Tk()
#
# # Title the window
# root.title("suck my cock")
# # Create the main frame widget that will hold our interface and arranging the grid to hold our widgets
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky='nsew')
# treeframe = ttk.Frame(mainframe, padding="3 3 10 10")
#
# treeframe.grid(column=0, row=0, columnspan=3)
#
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
#
# for x in range(10):
#     mainframe.columnconfigure(x, weight=1)
#     mainframe.rowconfigure(x, weight=1)
#
# columnse = ['Task', 'Worst time', 'Period']
#
# tree = Newtreeview(frame=treeframe, columns=columnse, show="headings")
#
# tree.tree.grid(column=0, row=0, sticky='new', columnspan=2)
#
# for index, item in enumerate(columnse):
#     tree.tree.column(index, stretch=True, width=100)
#     tree.tree.heading(item, text=item)
#
# Tinvoc = tk.IntVar()
# Tinvoc_E = ttk.Entry(mainframe, textvariable=Tinvoc)
# Tinvoc_E.grid(column=0, row=1, sticky='ew')
#
# Addinvoccol_B=tk.Button(
#     mainframe,
#     text='Set Invocations',
#     command=lambda: tree.setinvoccol(Tinvoc.get())
# )
#
# Run_B=tk.Button(
#     mainframe,
#     text='Run'
# )
# Addinvoccol_B.grid(column=1, row=1, sticky='ew')
# Run_B.grid(column=0, row=2, sticky='ew')
#
# FixFreq = tk.Checkbutton(mainframe, text='Fix Frequency')
# FixFreq.grid(column=1, row=2)
#
# tree.tree.bind('<Double-1>', tree.set_cell_value)
#
# filler = ['', '', '', '', '', '', '', '', '', '', '', '']
#
# for i in range(min(len(filler), len(filler))):
#     tree.tree.insert('', i, values=(filler[i]))
#
#
# if __name__ == '__main__':
#     root.mainloop()


# import numpy as np
#
# dat=[['0', 3, 1], ['b\n', 0, 0], ['c\n', 0, 0], ['d\n', 0, 0], ['e\n', 0, 0], ['f\n', 0, 0], ['g\n', 0, 0], ['h\n', 0, 0], ['i\n', 0, 0], ['', 0, 0], ['', 0, 0], ['', 0, 0]]
# data=[]
#
# # makes a new list with only rows that have data, and strips \n character
# for x in dat:
#     if x[0]:
#         x[0]=str(x[0]).strip('\n')
#         data.append(x)
#
# # makes a dictionary where each label gets assigned a unique number
# labeltonumber = {}
# labelkeys = range(len(data))
# for i in labelkeys:
#     labeltonumber[i] = data[i][0]
#
# print(labeltonumber)
# print(len(data),len(dat[0]))
#
# # replaces each label with its assigned number
# for index, x in enumerate(data):
#     x[0] = labelkeys[index]
#
# # replaces each label assigned number with its label
# # for index, x in enumerate(data):
# #     x[0] = labeltonumber[labelkeys[index]]
#
# # Transfer the data list into the numpy array standard for run time
# # # [[label1, worstcom1, period1, invocations1],
# # #  [label2, worstcom2, period2, invocations2]]
# ndat=np.zeros((len(data),len(dat[0])))
# for index1, x in enumerate(ndat):
#     for index2, y in enumerate(data[index1]):
#         x[index2]=y
#
# print(labelkeys[0])
#
# g=np.array([[0,0,0],[1,0,0], [2,0,0], [3,0,0], [4,0,0]])
# print(g)


# import tkinter as tk  # python 3.x
# # import Tkinter as tk # python 2.x
#
# class Example(tk.Frame):
#
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#
#         # valid percent substitutions (from the Tk entry man page)
#         # note: you only have to register the ones you need; this
#         # example registers them all for illustrative purposes
#         #
#         # %d = Type of action (1=insert, 0=delete, -1 for others)
#         # %i = index of char string to be inserted/deleted, or -1
#         # %P = value of the entry if the edit is allowed
#         # %s = value of entry prior to editing
#         # %S = the text string being inserted or deleted, if any
#         # %v = the type of validation that is currently set
#         # %V = the type of validation that triggered the callback
#         #      (key, focusin, focusout, forced)
#         # %W = the tk name of the widget
#
#         vcmd = (self.register(self.onValidate),
#                 '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
#         self.entry = tk.Entry(self, validate="key", validatecommand=vcmd)
#         self.text = tk.Text(self, height=10, width=40)
#         self.entry.pack(side="top", fill="x")
#         self.text.pack(side="bottom", fill="both", expand=True)
#
#     def onValidate(self, d, i, P, s, S, v, V, W):
#         self.text.delete("1.0", "end")
#         self.text.insert("end","OnValidate:\n")
#         self.text.insert("end","d='%s'\n" % d)
#         self.text.insert("end","i='%s'\n" % i)
#         self.text.insert("end","P='%s'\n" % P)
#         self.text.insert("end","s='%s'\n" % s)
#         self.text.insert("end","S='%s'\n" % S)
#         self.text.insert("end","v='%s'\n" % v)
#         self.text.insert("end","V='%s'\n" % V)
#         self.text.insert("end","W='%s'\n" % W)
#
#         # Disallow anything but lowercase letters
#         # if S == S.lower():
#         #     return True
#         if (S.isdigit()):
#             # self.bell()
#             return True
#         else:
#             self.bell()
#             return False
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     Example(root).pack(fill="both", expand=True)
#     root.mainloop()



# import tkinter as tk
# from tkinter import ttk
# from tkinter.messagebox import showinfo
#
# def popup_bonus():
#     win = tk.Toplevel()
#     win.wm_title("Window")
#
#     l = tk.Label(win, text="Input")
#     l.grid(row=0, column=0)
#
#     b = ttk.Button(win, text="Okay", command=win.destroy)
#     b.grid(row=1, column=0)
#
# def popup_showinfo():
#     showinfo("Window", "Hello World!")
#
# class Application(ttk.Frame):
#
#     def __init__(self, master):
#         ttk.Frame.__init__(self, master)
#         self.pack()
#
#         self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
#         self.button_bonus.pack()
#
#         self.button_showinfo = ttk.Button(self, text="Show Info", command=popup_showinfo)
#         self.button_showinfo.pack()
#
# root = tk.Tk()
#
# app = Application(root)
#
# root.mainloop()


# class hold():
#     def __init__(self, list):
#         self.info=list
#         self.cinfo=list
#
#     def print(self):
#         print(self.info, self.cinfo)
#
#     def change(self):
#         self.info = ['ass']
#
#     def changeb(self):
#         self.info = list(self.cinfo)
#         self.info = ['butts']
#
# m=hold(['1,2,3'])
# m.print()
# m.change()
# m.print()
# m.changeb()
# m.print()


# import matplotlib.colors as col
# import numpy as np
# import matplotlib.pyplot as plt
# import tkinter.filedialog as fd
# import tkinter as tk




"""
Main frontend GUI
"""

import tkinter as tk
from tkinter import ttk
import GUIbackend as GUI

# Create the tkinter window object called root
root = tk.Tk()

# Title the window
root.title("suck my cock")

# Create the main frame widget that will hold our interface and arranging the grid to hold our widgets
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='nsew')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Table widget displaying entered task information
columns = ('Task', 'Worst time', 'Period', 'Invo1', 'Invo2')
tree = ttk.Treeview(mainframe, columns=columns, show="headings")

tree.grid(column=0, row=0, sticky='new', columnspan=3)

tree.column(0, stretch=True, width=100)
tree.column(1, stretch=True, width=150)
tree.column(2, stretch=True, width=75)
tree.column(3, stretch=True, width=100)
tree.column(4, stretch=True, width=100)

tree.heading('Task', text='Task')
tree.heading('Worst time', text='Worst Computation')
tree.heading('Period', text='Period')
tree.heading('Invo1', text='Invocation 1')
tree.heading('Invo2', text='Invocation 2')


# Task information entry fields and labels
Tlable = tk.StringVar()
Tworst = tk.IntVar()
Tperiod = tk.IntVar()
Tinvoc1 = tk.IntVar()
Tinvoc2 = tk.IntVar()

Tlable_L = tk.Label(mainframe, text='Task Label')
Tworst_L = tk.Label(mainframe, text='Worst Case')
Tperiod_L = tk.Label(mainframe, text='Period')
Tinvoc1_L = tk.Label(mainframe, text='Invocation 1')
Tinvoc2_L = tk.Label(mainframe, text='Invocation 2')

Tlable_E = ttk.Entry(mainframe, textvariable=Tlable)
Tworst_E = ttk.Entry(mainframe, textvariable=Tworst)
Tperiod_E = ttk.Entry(mainframe, textvariable=Tperiod)
Tinvoc1_E = ttk.Entry(mainframe, textvariable=Tinvoc1)
Tinvoc2_E = ttk.Entry(mainframe, textvariable=Tinvoc2)

Tlable_L.grid(column=0, row=1, sticky='we')
Tworst_L.grid(column=0, row=2, sticky='we')
Tperiod_L.grid(column=0, row=3, sticky='we')
Tinvoc1_L.grid(column=0, row=4, sticky='we')
Tinvoc2_L.grid(column=0, row=5, sticky='we')

Tlable_E.grid(column=1, row=1, sticky='we')
Tworst_E.grid(column=1, row=2, sticky='we')
Tperiod_E.grid(column=1, row=3, sticky='we')
Tinvoc1_E.grid(column=1, row=4, sticky='we')
Tinvoc2_E.grid(column=1, row=5, sticky='we')


# Task Buttons
AddTask_B = tk.Button(
    mainframe,
    text='Add Task',
    command=lambda: GUI.addtolist(tree, Tlable.get(), Tworst.get(), Tperiod.get(), Tinvoc1.get(), Tinvoc2.get())
)
EditTask_B = tk.Button(mainframe, text='Edit Task', command=lambda: GUI.edittask(tree))
RemoveTask_B = tk.Button(mainframe, text='Remove Task', command=lambda: GUI.removetask(tree))

AddTask_B.grid(column=0, row=6, sticky='ew')
EditTask_B.grid(column=1, row=6, sticky='ew')
RemoveTask_B.grid(column=2, row=6, sticky='ew')

# Frequency Checkbox
FixFreq = tk.Checkbutton(mainframe, text='Fix Frequency')
FixFreq.grid(column=2, row=7)

# Run Button
RunTask_B = tk.Button(mainframe, text='RUN')
RunTask_B.grid(column=1, row=7, sticky='ew')

if __name__ == '__main__':
    root.mainloop()



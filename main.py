"""
Main frontend GUI
"""

import tkinter as tk
from tkinter import ttk
import GUIbackend as GUI
import numpy as np

# Create the tkinter window object called root
root = tk.Tk()

# Title the window
root.title("suck my cock")

# Create the main frame widget that will hold our interface and arranging the grid to hold our widgets
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='nsew')

treeframe = ttk.Frame(mainframe)
treeframe.grid(columnspan=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# Table widget displaying entered task information
columns = ['Task', 'Worst time', 'Period']
ntree = GUI.Newtreeview(mainframe, columns=columns, show="headings")

ntree.tree.grid(column=0, row=0, sticky='new', columnspan=3)

for index, item in enumerate(columns):
    ntree.tree.column(item, stretch=True, width=100, minwidth=100)
    ntree.tree.heading(item, text=item)

# Invocation amount entry field
Tinvoc = tk.IntVar()
Tinvoc_E = ttk.Entry(mainframe, textvariable=Tinvoc)
Tinvoc_E.grid(column=0, row=1, sticky='ew')

# Buttons
Addinvoccol_B = tk.Button(
    mainframe,
    text='Set Invocations',
    command=lambda: ntree.setinvoccol(Tinvoc.get())
)

Run_B = tk.Button(
    mainframe,
    text='Run simulation'
)

Addinvoccol_B.grid(column=1, row=1, sticky='ew')
Run_B.grid(column=0, row=2, sticky='ew')

printvalues_B = tk.Button(
    mainframe,
    text='print',
    command=lambda: ntree.getvalues()
)
printvalues_B.grid(column=0, row=3)
# Frequency Checkbox
FixFreq = tk.Checkbutton(mainframe, text='Fix Frequency')
FixFreq.grid(column=1, row=2)

ntree.tree.bind('<Double-1>', ntree.set_cell_value)

filler = ['', '', '', '', '', '', '', '', '', '', '', '']

for i in range(min(len(filler), len(filler))):
    ntree.tree.insert('', i, values=(filler[i]))
#
# filmore = ['red', '', '', '', '', '', '', '', '', '', '', '']
# for i in range(min(len(filler), len(filler))):
#     ntree.tree.insert('', i, values=(filler[i]))

if __name__ == '__main__':
    root.mainloop()



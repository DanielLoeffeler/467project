"""
Main frontend GUI
"""

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import GUIbackend as GUI
import numpy as np

# Create the tkinter window object called root
root = ThemedTk(theme='breeze')

# Title the window
root.title("Cycle Conserving EDF Algorithm Simulator")

# Create the main frame widget that will hold our interface and arranging the grid to hold our widgets
mainframe = ttk.Frame(root, padding="30 3 30 12")
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

# Invocation amount entry field describing label
Tinvoc_L = tk.Label(mainframe, text='Amount of Invocations')
Tinvoc_L.grid(column=0, row=1, sticky='ew')

# Invocation amount entry field
Tinvoc = tk.IntVar()
Tinvoc_E = ttk.Entry(mainframe, textvariable=Tinvoc)
Tinvoc_E.grid(column=1, row=1, sticky='ew')

# Buttons
Addinvoccol_B = tk.Button(
    mainframe,
    text='Set Invocations',
    command=lambda: ntree.setinvoccol(Tinvoc.get())
)

Savedat_B = tk.Button(
    mainframe,
    text='Save Tasks',
    command=lambda: ntree.getvalues()
)

Loaddat_B = tk.Button(
    mainframe,
    text='Load Tasks',
    command=lambda: ntree.loadfromlist()
)

Cleardat_B = tk.Button(
    mainframe,
    text='Clear Table',
    command=lambda: ntree.cleartreeview(True)
)

Run_B = tk.Button(
    mainframe,
    text='Run simulation',
    bg='forest green',
    command=lambda: ntree. createplot(freqvar.get())
)

Addinvoccol_B.grid(column=2, row=1, sticky='ew')
Loaddat_B.grid(column=0, row=2, sticky='ew')
Savedat_B.grid(column=1, row=2, sticky='ew')
Cleardat_B.grid(column=2, row=2, sticky='ew')
Run_B.grid(column=0, row=3, sticky='ew')

# Frequency Checkbox
freqvar = tk.IntVar()
FixFreq = tk.Checkbutton(mainframe, text='Fix Frequencies to 1Fmax, .75Fmax, and .5Fmax', variable=freqvar)
FixFreq.grid(column=1, row=3)

ntree.tree.bind('<Double-1>', ntree.set_cell_value)

filler = ['', '', '', '', '', '', '', '', '', '', '']
fillzero = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(min(len(filler), len(filler))):
    ntree.tree.insert('', i, values=(filler[i], fillzero[i], fillzero[i]))

if __name__ == '__main__':
    root.mainloop()



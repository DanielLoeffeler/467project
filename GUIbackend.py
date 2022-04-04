"""
The backend functionality of the GUI
"""
import tkinter as tk
from tkinter import ttk
import numpy as np

class Newtreeview():
	"""ttk treeview but with some more methods to control the amount of columns there are"""

	def __init__(self, frame, columns, show):
		self.frame = frame
		self.columns = columns
		self.show = show
		self.treedata = []
		self.tree = ttk.Treeview(frame, columns=columns, show=show)

	def printcolumns(self):
		print(self.columns)

	def loadfromlist(self, treedata):
		"""Takes a list with all the data to be stored in the treeview and puts it there"""
		for item in treedata:
			for dat in item:
				self.tree.insert('','end',dat)

	def getvalues(self):
		"""Creates a numpy array storing all of the information in the tree"""
		# # [[label1, worstcom1, period1, invocations1],
		# #  [label2, worstcom2, period2, invocations2]]
		self.treedata = []
		for index, line in enumerate(self.tree.get_children()):
			# print(line)
			# for value in self.tree.item(line)['values']:
			self.treedata.append(self.tree.item(line)['values'])
		print(self.treedata)

	def setinvoccol(self, invocs):
		"""Sets the amount of invocation columns to the given amount"""
		self.columns = ['Task', 'Worst time', 'Period']
		self.columns.extend(list(np.arange(1, invocs + 1)))

		self.getvalues()

		self.tree.destroy()
		self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings")

		for index, item in enumerate(self.columns):
			self.tree.column(item, stretch=True, width=100, minwidth=100)
			self.tree.heading(item, text=item)

		for index, item in enumerate(self.columns[3:]):
			index = 3 + index
			self.tree.column(index, stretch=True, width=100, minwidth=100)
			self.tree.heading(item, text='invocation ' + str(index - 2))

		self.tree.grid(column=0, row=0, sticky='new', columnspan=invocs + 3)

		self.tree.bind('<Double-1>', self.set_cell_value)

		# filler = ['', '', '', '', '', '', '', '', '', '', '', '']
		# for i in range(min(len(filler), len(filler))):
		# 	self.tree.insert('', 'end', values=(filler[i]))
		
		self.loadfromlist(self.treedata)

	def set_cell_value(self, event):
		"""The double click event that creates and entry field and ok button to enter info into a box"""
		try:
			# Find the column and row that is clicked on
			for item in self.tree.selection():
				item_text = self.tree.item(item, "values")
				column = self.tree.identify_column(event.x)
				row = self.tree.identify_row(event.y)
			cn = int(str(column).replace('#', ''))
			rn = int(str(row).replace('I', ''))

			# Finds the sum of pixels to the left of clicked on column
			colwidths = 0
			for co in range(cn - 1):
				if cn == 1:
					colwidths = 0
				else:
					colwidths += self.tree.column(co)['width']

			# Makes an entry form at the width of the column
			entryedit = tk.Text(self.frame, width=self.tree.column(cn - 1)['width'] // 7, height=1,
			                    font=("consolas", 10))
			entryedit.place(x=colwidths, y=6 + rn * 20)

			def saveedit():
				self.tree.set(item, column=column, value=entryedit.get(0.0, "end"))
				entryedit.destroy()
				okb.destroy()

			# Makes the OK button to the left of rightmost edge of the clicked on column
			okb = ttk.Button(self.frame, text='OK', width=4, command=saveedit)
			okb.place(x=colwidths + self.tree.column(cn - 1)['width'], y=2 + rn * 20)

		except:
			print('not in the treeview')


def createplot(stuff):
	# Creates the shit
	pass
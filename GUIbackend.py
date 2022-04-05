"""
The backend functionality of the GUI
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
import Math as EDF
import matplotlib.pyplot as plt
from math import ceil

class Newtreeview():
	"""ttk treeview but with some more methods to control the amount of columns there are"""

	def __init__(self, frame, columns, show):
		self.frame = frame
		self.columns = columns
		self.show = show
		self.treedata = np.array([[0, 3, 8, 2, 1],[1, 3, 10, 1, 1],[2, 1, 14, 1, 1]])
		self.labeltonumber = {0: 'a', 1: 'b', 2: 'c'}
		self.labelkeys = range(0, 3)
		self.tree = ttk.Treeview(frame, columns=columns, show=show)
		self.vcmd = (self.frame.register(self.onValidate),
		        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

	def printcolumns(self):
		print(self.columns)

	def cleartreeview(self,fill=False):
		"""Clears all values from tree view and restores it to zeros"""
		for line in self.tree.get_children():
			self.tree.delete(line)

		if fill:
			# Create empty rows for the user
			empties=[]
			for x in range(len(self.columns)):
				empties.append(0)
			empties[0]=''

			# Finds how many columns are filled and then filles zeroes below the last filled column with the diff from 15
			data = []
			for x in self.treedata:
				if x[0]:
					x[0] = str(x[0]).strip('\n')
					data.append(x)

			for index in range(11):
				niid = "I" + str(hex(index + 1)).lstrip("0x").title().zfill(3)  # Creates a row ID in the native 0xI001 hex form
				self.tree.insert('', index=index + 1, iid=niid, values=empties)

	def loadfromlist(self, treedata=None):
		"""Takes a list with all the data to be stored in the treeview and puts it there"""
		# If no data is passed to the function, use the classes stored data
		if treedata==None:
			treedata=self.treedata

		# for index, x in enumerate(treedata):
		#     x[0] = self.labeltonumber[self.labelkeys[index]] # Replaces each label assigned number with its label

		# Clear all information on the treeview currently
		self.cleartreeview()

		for index, item in enumerate(treedata):
			# Put the info in the relavent numpy array into a list to get string labels back
			iteml=[]
			for info in item:
				iteml.append(int(info))

			# If there are more columns than in the iteml list, fill with zeros
			# If there are more columns in iteml than in the treeview, strip those values
			if len(iteml)<len(self.columns):
				for x in range(len(self.columns)-len(iteml)):
					iteml.append(0)
			elif len(iteml)>len(self.columns):
				del iteml[int(len(self.columns)):]

			iteml[0] = self.labeltonumber[self.labelkeys[index]]  # Replaces each label assigned number with its label
			niid = "I"+str(hex(index+1)).lstrip("0x").title().zfill(3) # Creates a row ID in the native 0xI001 hex form
			self.tree.insert('',index=index+1, iid=niid, values=(iteml))

		# Create empty rows for the user
		empties=[]
		for x in range(len(self.columns)):
			empties.append(0)
		empties[0]=''

		# Fills everything beyond the data with zeroes
		for i in range(11-len(self.treedata)):
			# Creates a row ID in the native 0xI001 hex form
			niid = "I" + str(hex(i+len(self.treedata) + 1)).lstrip("0x").title().zfill(3)
			self.tree.insert('', index=i+len(self.treedata)+1, iid=niid, values=empties)

	def getvalues(self):
		"""Creates a numpy array storing all of the information in the tree"""
		# # [[label1, worstcom1, period1, invocations11, invocations12],
		# #  [label2, worstcom2, period2, invocations21, invocations22]]
		self.treedata = []
		for index, line in enumerate(self.tree.get_children()):
			self.treedata.append(self.tree.item(line)['values'])

		# Makes a new list with only rows that have data, and strips \n character
		data = []
		for x in self.treedata:
			if x[0]:
				x[0] = str(x[0]).strip('\n')
				data.append(x)

		# Makes a dictionary where each label gets assigned a unique number
		self.labeltonumber = {}
		self.labelkeys = range(len(data))
		for i in self.labelkeys:
			self.labeltonumber[i] = data[i][0]

		# Replaces each label with its assigned number
		for index, x in enumerate(data):
			x[0] = self.labelkeys[index]

		# Transfer the data list into the numpy array standard for run time
		# # [[label1, worstcom1, period1, invocations1],
		# #  [label2, worstcom2, period2, invocations2]]
		#print(len(data),len(self.treedata[0]))
		ndat = np.zeros((len(data), len(self.treedata[0])))
		#print(ndat.shape)
		try:
			for index1, x in enumerate(ndat):
				for index2, y in enumerate(data[index1]):
					if y == '\n': # If number field is left empty make it a zero
						y=0
					x[index2] = y

			self.treedata=ndat
		except IndexError:
			print("fill all the columns")
		except ValueError:
			print("only have int values in there boi")
		#print(self.treedata)

	def setinvoccol(self, invocs):
		"""Sets the amount of invocation columns to the given amount"""
		self.columns = ['Task', 'Worst time', 'Period']
		self.columns.extend(list(np.arange(1, invocs + 1)))

		self.getvalues() # Saves the values of the current table

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

		self.loadfromlist() # Loads the values in the tabel from before adding columns

	def set_cell_value(self, event):
		"""The double click event that creates and entry field and ok button to enter info into a box"""
		# try:
		# Find the column and row that is clicked on
		for item in self.tree.selection():
			item_text = self.tree.item(item, "values")
			column = self.tree.identify_column(event.x)
			row = self.tree.identify_row(event.y)
		#print(column, row)
		cn = int(str(column).replace('#', ''),16)
		rn = int(str(row).replace('I', ''),16)

		# Finds the sum of pixels to the left of clicked on column
		colwidths = 0
		for co in range(cn - 1):
			if cn == 1:
				colwidths = 0
			else:
				colwidths += self.tree.column(co)['width']
		#print(cn,rn)
		# Makes an entry form at the width of the column, that only allows numbers in any column after the first
		if cn>1:
			entryedit = tk.Entry(self.frame,
			                    width=self.tree.column(cn - 1)['width'] // 7,
			                    # height=1,
			                    font=("consolas", 10),
			                    validate='key',
			                    validatecommand=self.vcmd)
		else:
			entryedit = tk.Entry(self.frame,
			                    width=self.tree.column(cn - 1)['width'] // 7,
			                    # height=1,
			                    font=("consolas", 10))

		entryedit.place(x=colwidths, y=11 + rn * 20)
		def saveedit():
			self.tree.set(item, column=column, value=entryedit.get())
			entryedit.destroy()
			okb.destroy()

		# Makes the OK button to the left of rightmost edge of the clicked on column
		okb = ttk.Button(self.frame, text='OK', width=4, command=saveedit)
		okb.place(x=colwidths + self.tree.column(cn - 1)['width'], y=2 + rn * 20)

		# except:
		# 	print('not in the treeview')

	def onValidate(self, d, i, P, s, S, v, V, W):
		# self.text.delete("1.0", "end")
		# self.text.insert("end", "OnValidate:\n")
		# self.text.insert("end", "d='%s'\n" % d)
		# self.text.insert("end", "i='%s'\n" % i)
		# self.text.insert("end", "P='%s'\n" % P)
		# self.text.insert("end", "s='%s'\n" % s)
		# self.text.insert("end", "S='%s'\n" % S)
		# self.text.insert("end", "v='%s'\n" % v)
		# self.text.insert("end", "V='%s'\n" % V)
		# self.text.insert("end", "W='%s'\n" % W)

		if (S.isdigit()):
			return True
		else:
			# self.bell()
			return False

	def makegraph(self, given, calculated, resolution, endpoint, ltn, lk):
		def make_yval(ranges, res, xrange):
			# Takes the instance array and returns an array containing the frequency values for each unit of time
			# between the start and the stop
			taskval = np.zeros(xrange.size)

			for i, item in enumerate(ranges):
				taskval[int(item[0] // res):int(item[1] // res)] = item[2]
				#print(int(item[0] // res))
			return taskval

		# Makes all the poitn on x axis for data
		xrng = np.arange(0, endpoint, resolution)

		# Take calculated result and break it into one 3D array where each array one step in is all one task
		hold = np.zeros((given.shape[0], given.shape[1] - 3, 3))

		for taskamt in range(given.shape[0]):
			# for invocamt in range(given.shape[1]-3):
			for index, x in enumerate(calculated[calculated[:, -1] == taskamt]):
				hold[taskamt, index] = x[0:3]

		colourlist = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
		yvals = []

		ax1 = plt.subplot()
		#print(calculated)
		# extract all the xticks from calculated array
		xticks = []
		for item in calculated:
			for x in range(2):
				# print(item[x])
				xticks.append(item[x])
		# xticks=[round(num, 1) for num in xticks]
		ax1.set_xticks(xticks, rotation=45)

		# extracts all the yticks from calculated array
		yticks = []
		for item in calculated:
			yticks.append(item[2])
		yticks = [round(num, 2) for num in yticks]
		ax1.set_yticks(yticks)

		yxpos = []
		for item in calculated:
			yxpos.append(item[0])

		# for index, x in enumerate(given):
		#     x[0] = self.labeltonumber[self.labelkeys[index]] # Replaces each label assigned number with its label

		names = []
		for index, x in enumerate(given):
			names.append(str(ltn[lk[index]]))  # Replaces each label assigned number with its label
		print(names)

		# Add each task array to the plot with a unique colour
		for index, tasklist in enumerate(hold):
			yvals = make_yval(tasklist, resolution, xrng)
			plt.bar(xrng, yvals, width=resolution, align="center", color=colourlist[index])

		for index, value in enumerate(yticks):
			plt.text(yxpos[index], value, str(value))

		plt.legend(names, loc='top right')
		plt.xticks(rotation=90)
		plt.show()

	def createplot(self, freqflag):
		# Creates the shit
		self.getvalues()
		# print(self.treedata,freqflag)

		calculatede = EDF.Run(self.treedata)

		# Remove all rows with only zeroes in them
		calculatede = calculatede[~np.all(calculatede == 0, axis=1)]

		# Remove all rows where the last item is -1
		calculatede = calculatede[calculatede[:, -1] != -1]

		resolutione = 0.001

		endpointe = ceil(calculatede[-1,-3])+1

		self.makegraph(self.treedata, calculatede, resolutione, endpointe, self.labeltonumber, self.labelkeys)

"""
The backend functionality of the GUI
"""


def addtolist(tree, Tlabel, Tworst, Tperiod, Tinvoc1, Tinvoc2):
	# Button function. Adds entered information to the tree list then clears the information fields
	tree.insert('', 'end', values=(Tlabel, Tworst, Tperiod, Tinvoc1, Tinvoc2))


def edittask(tree):
	# Button opens a menu to edit the selected task in the tree
	pass


def removetask(tree):
	# Button removes task selected in tree
	pass
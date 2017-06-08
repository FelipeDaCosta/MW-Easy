import Tkinter as tk

DIAS = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado']
HORARIOS = ['8 - 10', '10 - 12', '12 - 14', '14 - 16', '16 - 18']

HIGHLIGHT_CELL = "#FAFF6B"
SELECTED_CELL = "#CE2D2D"
BACKGROUND_COLOR = "white"


CIRCLE_RADIUS = 5
CIRCLE_H_OFFSET = 20


class Cell(tk.Canvas, object):
	"""
	
	"""
	def __init__(self, parent, text, row, col, width=150, height=70, background=BACKGROUND_COLOR, clickable=True):
		super(Cell, self).__init__(parent, bd=0, highlightbackground="black", width=width, height=height, background=background)
		self.w = int(self['width'])
		self.h = int(self['height'])
		self.row = row
		self.col = col
		self.put_text(text)
		self.grid(row=row, column=col)
		self.circles = []
		self.clicked = False
		if clickable:
			self.bind("<Enter>", lambda event: self.enter(event))
			self.bind("<Leave>", lambda event: self.leave(event))
			self.bind("<Button-1>", lambda event: self.click(event))

	def enter(self, event):
		if not self.clicked:
			self.draw_background(HIGHLIGHT_CELL)

	def leave(self, event):
		if not self.clicked:
			self.draw_background(BACKGROUND_COLOR)

	def click(self, event):
		if not self.clicked:
			self.draw_background(SELECTED_CELL)
		else:
			self.draw_background(BACKGROUND_COLOR)
		self.clicked = not self.clicked

	def draw_background(self, color):
		self.configure(bg=color)

	def draw_circle(self, x, y, radius, color):
		self.create_oval(x+radius, y-radius, x-radius, y+radius, fill=color)

	def draw_all_circles(self):
		for i in self.circles:
			self.draw_circle(self.w/2, self.h/2 + CIRCLE_H_OFFSET, CIRCLE_RADIUS, i)

	def put_text(self, text):
		self.create_text(self.w/2, self.h/2, text=text)


class Table(tk.Frame, object):
	"""

	"""
	def __init__(self, parent):
		super(Table, self).__init__(parent)
		self.cells = []
		for i, dia in enumerate(DIAS):
			Cell(self, dia, 0, i, height=40, background="#E3ECF9", clickable=False) # Escrevendo dias da semana
		for i, horario in enumerate(HORARIOS):
			self.cells.append([])
			for j, dia in enumerate(DIAS):
				self.cells[i].append(Cell(self,horario, i+1, j))
		self.pack()

	def get_selected_cells(self):
		total = []
		for row in self.cells:
			for cell in row:
				if cell.clicked:
					total.append(str(cell.row) + str(cell.col))



"""
Modulo que contem as classes e funcoes responsaveis pelo funcionamento da
interface grafica
"""

import Tkinter as tk
import DataHandler as dh

# TEMP
def do_nothing():
	pass

def on_select(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	print 'You selected item %d: %s' % (index, value)

def on_double(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	print 'DOUBLE CLICK ON %d: %s' % (index, value)

lista_teste = ["Calculo 1", "Estrutura de dados", "Computacao Basica", "OAC"]


## Classes ##

class Lista_materias(tk.Listbox, object):
	"""
	Classe da lista de materias que fica do lado direito (>) da GUI
	"""
	def __init__(self, frame, materias=None):
		super(Lista_materias, self).__init__(frame)
		self.populate(materias)
		self.grid(sticky=tk.E + tk.W + tk.S + tk.N)
		self.bind('<<ListboxSelect>>', on_select)
		self.bind('<Double-Button-1>', on_double)

	def populate(self, materias):
		"""
		Recebe uma lista e popula a listbox com o elemento da lista
		"""
		if materias is not None:
			for i, mat in enumerate(materias):
				self.insert(i, mat.nome)

class Menubar(tk.Menu, object):
	"""
	Classe do menu da barra principal
	"""
	def __init__(self, frame):
		super(Menubar, self).__init__(frame)
		self.create_file_menubar()
		self.create_materias_menu()

	def create_file_menubar(self):
		"""
		Define as opcoes 'file' na barra do menu principal
		"""
		filemenu = tk.Menu(self, tearoff=0)
		filemenu.add_command(label="New", command=do_nothing)
		filemenu.add_command(label="Open", command=do_nothing)
		filemenu.add_command(label="Save", command=do_nothing)
		filemenu.add_command(label="Save as...", command=do_nothing)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=do_nothing)
		self.add_cascade(label="File", menu=filemenu)

	def create_materias_menu(self):
		"""
		Define as opcoes de 'materias' na barra do menu principal
		"""
		materiasmenu = tk.Menu(self, tearoff=0)
		materiasmenu.add_command(label="Atualizar", command=do_nothing)
		materiasmenu.add_command(label="Cursos", command=do_nothing)
		materiasmenu.add_command(label="Sei la", command=do_nothing)
		self.add_cascade(label="Materias", menu=materiasmenu)

class Filtro(object):
	"""
	Contem todos os checkbuttons usados para filtrar as materias
	"""
	def __init__(self, frame):
		self.filtro_check = tk.Checkbutton(frame, text="filtro")
		self.filtro_check2 = tk.Checkbutton(frame, text="filtro2")
		self.filtro_check2.pack()
		self.filtro_check.pack()




class Main_window(object):
	def __init__(self):
		self.raiz = tk.Tk()
		self.raiz.rowconfigure(0, weight=1)
		self.raiz.columnconfigure(0, weight=1)
		self.dataHandler = dh.DataHandler()
		self.w = self.raiz.winfo_screenwidth()
		self.h = self.raiz.winfo_screenheight()

		# Menu da barra principal
		self.menubar = Menubar(self.raiz)
		self.raiz.config(menu=self.menubar)

		# Frames
		self.frame_materias = tk.Frame(self.raiz)
		#self.frame_filter = tk.Frame(self.raiz)
		#self.filter = Filtro(self.frame_filter)
		self.frame_materias.rowconfigure(0,weight=1)

		# Lista de materias
		self.list_box = Lista_materias(self.frame_materias, materias=self.dataHandler.read_list())
		self.frame_materias.grid(sticky=tk.E + tk.N + tk.S)
		#self.frame_filter.grid(row=1, column=0,sticky=tk.S)



	def run(self):
		"""
		Inicia a GUI
		"""
		self.raiz.mainloop()



a = Main_window()
a.run()
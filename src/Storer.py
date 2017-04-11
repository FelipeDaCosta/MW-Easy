"""
	Author: Felipe da Costa Malaquias
	Reponsavel por guardar e ler todas as informacoes adquiridas online.
	Utiliza Pickle
	Lista de arquivos craidos:
		data_dict.mw -> Guarda um dicionario (codigo_materia : materia)
		data_list.mw -> Guarda uma lista de materias (temp)
	(https://docs.python.org/2/library/shelve.html)
"""

import cPickle
import os

class Storer(object):
	def __init__(self, scraper):
		self.DICT_FILE  = os.path.join("..", "data", "data_dict.mw")
		self.LIST_FILE = os.path.join("..", "data", "data_list.mw")
		self.scraper = scraper


	# Pega os arquivos da web e guarda a lista e o dicionario
	def get_and_store(self, codigo_curso, verbose=False):
		lista_materias = a.get_materias(codigo_curso)
		lista_final_materias = []

		for i in lista_materias:
			mat = Materia(i[1], i[0], a)
			lista_final_materias.append(mat)
			if verbose:
				print i[0]

		dicionario_final_materias = dict((i.codigo, i) for i in lista_final_materias)

		cPickle.dump(lista_final_materias, open(self.LIST_FILE, "wb"))
		cPickle.dump(dicionario_final_materias, open(self.DICT_FILE, "wb"))
		

	# Le o arquivo read_list.mw e retorna a lista. Retorna None caso o arquivo n exista
	def read_list(self):
		if os.path.isfile(self.LIST_FILE):
			list_file = cPickle.load(open(self.LIST_FILE, "rb"))
			return list_file
		return None

	# Le o arquivo data_dict.mw e retorna o dicionario. Retorna None caso o arquivo n exista
	def read_dict(self):
		if os.path.isfile(self.DICT_FILE):
			dict_file = cPickle.load(open(self.DICT_FILE,"rb"))
			return dict_file
		return None



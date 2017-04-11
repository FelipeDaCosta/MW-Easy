# Author : Felipe da Costa Malaquias
import Turma
import Scraper

class Materia(object):

	def __init__(self, nome, codigo, scraper):
		self.scraper = scraper
		self.nome = nome
		self.codigo = codigo
		self.turmas = []
		self.get_oferta()
		

	def get_oferta(self):
		new_oferta = self.scraper.get_oferta(self.codigo)
		if new_oferta != None:
			self.turmas = new_oferta
		else:
			self.turmas = []

	def add_turma(self, turma):
		if type(a) is list:
			turmas.extend(turma)
		elif type(a) is Turma.Turma:
			turmas.append(turma)
	
	def print_oferta(self):
		if self.turmas != None and self.turmas != []:
			for turma in self.turmas:
				turma.print_info()
				print '\n'	
		else:
			print "Erro self.turmas == None"

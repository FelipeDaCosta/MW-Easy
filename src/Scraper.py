# -*- coding: utf-8 -*-
# Author : Felipe da Costa Malaquias

"""
	Scraper eh a classe responsavel pela requisicao e parsing dos dados online
"""

import requests
import bs4
import pickle
import re
import pprint
import io
import time
import os
import random
from Turma import Turma

class Scraper(object):
	def __init__(self):
		self.BASE_URL = 'https://matriculaweb.unb.br/graduacao/'
		self.CURSOS_URL = 'https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod=1'
		self.BASE_CURSO_URL = 'https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod='
		self.BASE_OFERTA = 'https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod='
		# Usado para fazer o parsing dos dias
		self.DIAS = [u'segunda', u'terça',u'quarta', u'quinta', u'sexta', u'sábado'] 
		# Palavra usada para encontrar informacoes sobre vagas
		self.KEY_WORD_VAGAS = u'totalvagas' 
		# Para achar o numero de creditos da disciplina
		self.KEY_WORD_CREDITOS = u'créditos'
		# Depois que encontrar essa keyword a proxima palavra eh o nome do professor
		self.KEY_WORD_NOME_PROF = u'sáb'

		# Usando proxies pra nao aparecer varios requests do msm IP no servidor
		# Isso + a espera de 1 segundo a cada request vai diminuir as chances de dar merda
		# A lista de proxies fica no arquivo http_proxies.txt
		self.proxies = []
		if(os.path.isfile("http_proxies.txt")):
			with open("http_proxies.txt", "r") as f:
				self.proxies = f.read().split()


	# Faz o request da pagina. Retorna um request object. Caso a conexao falhe retorna None
	def make_request(self, link):
		if(link == None):
			return None
		# Esperar no minimo 1 segundo entre requests pra nao fazer varios de uma vez
		# E ser confundido com um DoS
		time.sleep(1) 
		try:
			r = requests.get(link, proxies={'http':'182.253.197.60'})
			return r
		except requests.ConnectionError:
			print 'Conexao falhou ao tentar requisitar o link ' + link
			return None

	# Retorna uma lista contendo tuplas (codigo, nome do curso)
	def get_all_cursos(self, verbose=False):
		get_codigo_curso = lambda  x : x[21:] # Lambda para pegar o codigo do curso
		all_cursos = []
		r = self.make_request(self.CURSOS_URL)
		if(r == None):
			return None
		soup = bs4.BeautifulSoup(r.text, 'html.parser')

		# Busca so na lista de cursos
		table = soup.find('table', {'class','FrameCinza'})

		for link in table.find_all('a'):
			if verbose:
				print(link.get('href') + ' ' + link.getText())
				print(get_codigo_curso(link.get('href')) + ' ' + link.getText())
			all_cursos.append((get_codigo_curso(link.get('href')), link.getText()))
		return all_cursos

	# Recebe o codigo do curso e retorna a url para a pagina com todas as materias do curso
	def get_curriculo(self, num, verbose=False):
		r = self.make_request(self.BASE_CURSO_URL + str(num))
		if(r == None):
			return None
		# Regex vai ser mais facil que bs aqui eu acho
		regex_pattern = re.compile(r'curriculo\.aspx\?cod=[0-9]*')
		match = regex_pattern.search(r.text)
		if verbose:
			print match.group()
		return self.BASE_URL + match.group()

	def get_codigo_materia(self, href):
		return href[20:]

	# Recebe o codigo de um curso e retorna uma lista de tuplas (codigo, nome da materia)
	def get_materias(self, codigo, verbose=False):
		all_materias = []
		url = self.get_curriculo(codigo) # Pega o link do currculo da materia
		r = self.make_request(url)
		if(r == None):
			return None
		soup = bs4.BeautifulSoup(r.text, 'html.parser')

		# Ta meio "Gambiarrado" isso aqui. Desse jeito vai ser dificil separar obrigatorias de
		# optativas, depois preciso dar uma ajeitada nisso
		for link in soup.find_all('a'):
			if len(link.getText()) > 0 and link.getText()[0].isdigit(): # Gambiarra
				if verbose:
					print link.getText()
				all_materias.append((link.getText()[:6], link.getText()[8:].strip()))

		if verbose:
			print 'LISTA DE MATERIAS:'
			pprint.pprint(all_materias)

		return all_materias

	# Se a informacao se tratar do dia e horario da aula retorna true. Usado na procura em <div>
	def is_dia_da_semana(self, string):
		for dia in self.DIAS:
			if string.lower().startswith(dia):
				return True
		return False

	# Se a informacao se tratar das vagas da turma retorna true. Usado na procura em <td>
	def is_info_vagas(self, string):
		if string.lower().startswith(self.KEY_WORD_VAGAS):
			return True
		return False

	# NAO INDICA ONDE TEM AS INFORMACOES DA TURMA. So diz que a proxima info vai ser a da turma
	# Usado na pprocura em <td>
	# Nao estou utilizando essa funcao por agora mas vou deixar aqui just in case
	def next_is_info_turma(self, string):
		if string.lower().startswith(self.KEY_WORD_TURMA):
			return True
		return False

	# Indica a turma. nao precisa de keyword, so procura strings com 1 ou 2 letras
	# Usado em <div>
	def is_info_turma(self, string):
		string = string.strip()
		if len(string) == 2 or len(string) == 1:
			if string.isupper():
				return True
		return False

	# NAO INDICA ONDE TEM AS INFORMACOES DO PROFESSOR.
	# No html o nome do prof vem logo apos um "SAB", portanto, essa funcao retorna true ao encontrar esse sab
	# Usado na procura em <td>
	def next_is_info_professor(self, string):
		if string.lower().startswith(self.KEY_WORD_NOME_PROF):
			return True
		return False



	# Esse metodo faz o uso do famoso metodo da Gambiarra
	# Pego todos os <div>'s do html pra achar os horarios da materia
	# Dps pego todos os <td>'s pra achar o numero de vagas turma e nome do professor
	# O numero de creditos da materia eu acho usando regex
	# (Eu nao vou deduzir o numero de creditos pelas horas de aula pq vai que tem materia de 1 hora/1 credito

	# TA MUITO BAGUNCADO ESSA PORRA AQUI TEM Q AJEITAR

	def get_oferta(self, codigo, verbose=False):
		r = self.make_request(self.BASE_OFERTA + str(codigo))
		if(r == None):
			return None
		soup = bs4.BeautifulSoup(r.text, 'html.parser')
		turmas = [] # Vai ser retornado ao final do metodo. Vai conter todas as turmas de uma determinada materia
		regex_pattern = re.compile(r'\(Teor-Prat-Ext-Est\)(\w+)-(\w+)-(\w+)-(\w+)')
		creditos = None

		div = []
		first = True # O numero de creditos vem na primeira div encontrada, vamos usar essa flag pra fazer o regex
		cur_turma = None
		for data_div in soup.find_all('div'):
			info = data_div.getText().strip()
			if first:
				creditos = regex_pattern.search(info)
				first = False # Encontra no primeiro e pronto
			if self.is_info_turma(info):
				if cur_turma != None:
					turmas.append(cur_turma)
				cur_turma = Turma(turma=info)
			if self.is_dia_da_semana(info):
				cur_turma.set_horarios(info)
		if cur_turma != None:
			turmas.append(cur_turma)	

		# Aqui ja a string de turmas ja vai estar formada
		# Vamos usar essa variavel para andar pela string de turmas
		cur_turma = 0 
		# Essa flag vai avisar se o nome do professor eh a proxima informacao
		next_is_professor = False
		for data_td in soup.find_all('td'):
			info = data_td.getText()
			# Esse if aqui eu n entendi bem mas sem ele n funciona entao eh noiz
			if info != None:
				info = info.strip()
			else:
				continue
		
			# Se a proxima info eh o nome do professor (determinado pela func next_is_info_prof)
			if next_is_professor and info:
				turmas[cur_turma].set_professor(info)
				next_is_professor = False
				cur_turma += 1
			if self.is_info_vagas(info):
				turmas[cur_turma].set_vagas(info)
			if self.next_is_info_professor(info):
				next_is_professor = True

		return turmas





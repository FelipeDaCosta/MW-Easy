# -*- coding: utf-8 -*-
# Author : Felipe da Costa Malaquias

"""
    Modulo responsavel por lidar fornecer os dados do matricula web
    para a aplicacao, seja pegando esses dados online utilizando
    a classe Scraper ou pegando os dados guardados nos arquivos
"""


import re
import pprint
import time
import os
import random
import requests
import bs4
from Turma import Turma

#######################################################
#####################  GLOBAIS ########################
#######################################################

BASE_URL = 'https://matriculaweb.unb.br/graduacao/'
CURSOS_URL = 'https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod=1'
BASE_CURSO_URL = 'https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod='
BASE_OFERTA = 'https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod='
# Usado para fazer o parsing dos dias
DIAS = [u'segunda', u'terça', u'quarta', u'quinta', u'sexta', u'sábado']
# Palavra usada para encontrar informacoes sobre vagas
KEY_WORD_VAGAS = u'totalvagas'
# Depois que encontrar essa keyword a proxima palavra eh o nome do professor
KEY_WORD_NOME_PROF = u'sáb'


#######################################################
################## FUNCOES AUXILIARES #################
#######################################################

def is_dia_da_semana(string):
    """
        Se a informacao se tratar do dia e horario da aula retorna true. Usado na procura em <div>
    """
    for dia in DIAS:
        if string.lower().startswith(dia):
            return True
    return False

def is_info_vagas(string):
    """
        Se a informacao se tratar das vagas da turma retorna true. Usado na procura em <td>
    """
    if string.lower().startswith(KEY_WORD_VAGAS):
        return True
    return False

def is_info_turma(string):
    """
        Indica a turma. nao precisa de keyword, so procura strings com 1 ou 2 letras, Usado em <div>
    """
    string = string.strip()
    if len(string) == 2 or len(string) == 1:
        if string.isupper():
            return True
    return False

def next_is_info_professor(string):
    """
        NAO INDICA ONDE TEM AS INFORMACOES DO PROFESSOR.
        Retorna true se encontrar "SAB" no html. As informacoes do prof vem logo dps
    """
    if string.lower().startswith(KEY_WORD_NOME_PROF):
        return True
    return False



#######################################################
####################### CLASSES #######################
#######################################################


class Scraper(object):
    """
        Responsavel por pegar os dados online e fazer o parsing
        Tabem gerencia a lista de proxies (caso exista)
    """
    def __init__(self):
        # Usando proxies pra nao aparecer varios requests do msm IP no servidor
        # Isso + a espera de 1 segundo a cada request vai diminuir as chances de dar merda
        # A lista de proxies fica no arquivo http_proxies.txt
        self.proxies = []
        if os.path.isfile("http_proxies.txt"):
            with open("http_proxies.txt", "r") as proxy_list:
                self.proxies = proxy_list.read().split()


    def make_request(self, link):
        """
            Faz o request do link passado, retorna None caso algum erro aconteca
        """
        if link is None:
            return None
        # Esperar no minimo 1 segundo entre requests pra nao fazer varios de uma vez
        # E ser confundido com um DoS
        time.sleep(1)
        i = 0
        while True:
            try:
                if len(self.proxies) > 1 and i < 3:
                    proxy = random.choice(self.proxies)
                    print 'Fazendo request pelo proxy ' + proxy
                    request = requests.get(link, proxies={'http':proxy})
                else:
                    request = requests.get(link)
                return request
            except requests.exceptions.ProxyError:
                print 'Proxy nao esta funcionando'
                self.proxies.remove(proxy)
                i += 1
            except requests.ConnectionError: # Erro de conexao
                print 'Conexao falhou ao tentar requisitar o link ' + link
                return None


    def get_all_cursos(self, verbose=False):
        """
            Retorna uma lista contendo tuplas (codigo, nome do curso)
        """
        get_codigo_curso = lambda  x: x[21:] # Lambda para pegar o codigo do curso
        all_cursos = []
        request = self.make_request(CURSOS_URL)
        if request is None:
            return None
        soup = bs4.BeautifulSoup(request.text, 'html.parser')

        # Busca so na lista de cursos
        table = soup.find('table', {'class', 'FrameCinza'})

        for link in table.find_all('a'):
            if verbose:
                print link.get('href') + ' ' + link.getText()
                print get_codigo_curso(link.get('href')) + ' ' + link.getText()
            all_cursos.append((get_codigo_curso(link.get('href')), link.getText()))
        return all_cursos


    def get_curriculo(self, num, verbose=False):
        """
            Recebe o codigo do curso e retorna a url para a pagina com todas as materias do curso
        """
        request = self.make_request(BASE_CURSO_URL + str(num))
        if request is None:
            return None
        # Regex vai ser mais facil que bs aqui eu acho
        regex_pattern = re.compile(r'curriculo\.aspx\?cod=[0-9]*')
        match = regex_pattern.search(request.text)
        if verbose:
            print match.group()
        return BASE_URL + match.group()

    def get_materias(self, codigo, verbose=False):
        """
            Recebe o codigo de um curso e retorna uma lista de tuplas (codigo, nome da materia)
        """
        all_materias = []
        url = self.get_curriculo(codigo) # Pega o link do currculo da materia
        request = self.make_request(url)
        if request is None:
            return None
        soup = bs4.BeautifulSoup(request.text, 'html.parser')

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


    def get_oferta(self, codigo, verbose=False):
        """
            Retorna uma lista contendo todas as ofertas. Precisa fazer uma busca em <div>
            e uma busca em <td> para pegar todas as informacoes
            <div> -> pega dias da semana e horarios
            <td> -> pega informacoes relacionadas a vagas e o nome do prof.
        """
        request = self.make_request(BASE_OFERTA + str(codigo))
        if request is None:
            return None
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        regex_pattern = re.compile(r'\(Teor-Prat-Ext-Est\)(\w+)-(\w+)-(\w+)-(\w+)')
        data_div = soup.find_all('div') # Sera usado mais tarde

        turmas = []
        cur_turma = None
        for div_element in data_div:
            info = div_element.getText().strip()
            if  is_info_turma(info):
                if cur_turma is not None:
                    turmas.append(cur_turma)
                cur_turma = Turma(turma=info)
            if is_dia_da_semana(info):
                cur_turma.set_horarios(info)
        if cur_turma != None: # A ultima classe nao eh adicionada no loop
            turmas.append(cur_turma)

        contador_turma = 0
        next_is_professor = False
        for td_element in soup.find_all('td'):
            info = td_element.getText().strip()
            if next_is_professor and info:
                turmas[contador_turma].set_professor(info)
                next_is_professor = False
                contador_turma += 1
            if is_info_vagas(info):
                turmas[contador_turma].set_vagas(info)
            if next_is_info_professor(info):
                next_is_professor = True

        # Numero de creditos vem sempre no primeiro div
        creditos = regex_pattern.search(data_div[0].getText().strip())
        if creditos is None:
            creditos = 0
        if verbose:
            print creditos
            print turmas

        return creditos, turmas

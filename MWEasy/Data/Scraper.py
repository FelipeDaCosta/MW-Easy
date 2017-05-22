# -*- coding: utf-8 -*-
# Author : Felipe da Costa Malaquias

"""
    Scraper usado para pegar informacoes do site matriculaweb.unb.br
"""

import re
import pprint
import os
import random
import requests
import bs4
from Materia import Turma

############ Constantes ############

# URLs base
BASE_URL = 'https://matriculaweb.unb.br/graduacao/'
BASE_CURSO_URL = BASE_URL + 'curso_dados.aspx?cod='
BASE_OFERTA = BASE_URL + 'oferta_dados.aspx?cod='

# URL com todos os cursos de graduacao
CURSOS_URL = BASE_URL + 'curso_rel.aspx?cod=1'

# Keywords usadas para identificar dados durante o parsing
DIAS = [u'segunda', u'terça', u'quarta', u'quinta', u'sexta', u'sábado']
KEY_WORD_VAGAS = u'totalvagas'
KEY_WORD_NOME_PROF = u'sáb' # nome do professor vem depois de sab.



############ Funcoes Auxiliares ############

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


def get_info_turmas(data_div, data_td):
    """
    Retorna uma lista com todas as turmas de uma materia.
    """
    # Turma, horarios
    turmas = []
    cur_turma = None
    for div_element in data_div:
        info = div_element.getText().strip()
        if  is_info_turma(info):
            if cur_turma is not None: # Encontrou outra Turma
                turmas.append(cur_turma)
            cur_turma = Turma(turma=info)
        if is_dia_da_semana(info):
            cur_turma.set_horarios(info)
    if cur_turma != None: # A ultima turma nao eh adicionada no loop
        turmas.append(cur_turma)

    # Professor, vagas
    contador_turma = 0
    next_is_professor = False
    for td_element in data_td:
        info = td_element.getText().strip()
        if next_is_professor and info:
            turmas[contador_turma].set_professor(info)
            next_is_professor = False
            contador_turma += 1
        if is_info_vagas(info):
            vagas_restantes = info.split()
            turmas[contador_turma].set_vagas(int(filter(unicode.isdigit, vagas_restantes[2])))
        if next_is_info_professor(info):
            next_is_professor = True
    return turmas


############ Classes ############

class Scraper(object):
    """
        Pega os dados online do site matriculaweb.unb.br
    """
    def __init__(self):
        """
            Inicia uma lista de proxies caso exista o arquivo http_proxies.txt no diretorio.
        """
        self.proxies = []
        if os.path.isfile("http_proxies.txt"):
            with open("http_proxies.txt", "r") as proxy_list:
                self.proxies = proxy_list.read().split()



    def make_request(self, link):
        """
            Faz o request do link passado, retorna None caso algum erro aconteca.

            Se existir uma lista de proxies, ira utilizar um desses proxies. No caso do
            proxy nao estar ativo, retira ele da lista e faz um request normal

            Param:
                link - String contendo a url da request

            Return:
                Response obj do link passado ou None no caso de falha
        """
        try:
            if len(self.proxies) > 0:
                proxy = random.choice(self.proxies)
                print 'Fazendo request pelo proxy ' + proxy
                request = requests.get(link, proxies={'http':proxy})
            else:
                request = requests.get(link)
            return request
        except requests.exceptions.ProxyError: # Erro no proxy
            print 'Proxy nao esta funcionando'
            self.proxies.remove(proxy)
        except requests.ConnectionError: # Erro de conexao
            print 'Conexao falhou ao tentar requisitar o link ' + link
            return None


    def get_all_cursos(self, verbose=False):
        """
            Faz o scraping do link em CURSOS_URL. Retorna uma lista contendo
            tuplas no formato (codigo do curso, nome do curso). O nome curso
            vem em UTF-8.

            Return:
                Tupla contendo codigo e nome de todos os cursos de graduacao.
                None caso haja erro (geralmente de conexao).
        """
        get_codigo_curso = lambda  x: x[21:]
        all_cursos = []
        request = self.make_request(CURSOS_URL)
        if request is None:
            return None
        soup = bs4.BeautifulSoup(request.text, 'html.parser')

        # Table contendo a lista dos cursos
        table = soup.find('table', {'class', 'FrameCinza'})

        for link in table.find_all('a'):
            if verbose:
                print link.get('href') + ' ' + link.getText()
                print get_codigo_curso(link.get('href')) + ' ' + link.getText()
            all_cursos.append((get_codigo_curso(link.get('href')), link.getText()))
        return all_cursos

    def get_curriculo_url(self, codigo, verbose=False):
        """
            Retorna a url da pagina de curriculos de um curso.

            Param:
                codigo - Codigo do curso (em string ou inteiro)
            Return:
                Pagina do curriculo do curso
                None em caso de erro
        """
        request = self.make_request(BASE_CURSO_URL + str(codigo))
        if request is None:
            return None
        # Regex vai ser mais facil que bs aqui eu acho
        regex_pattern = re.compile(r'curriculo\.aspx\?cod=[0-9]*')
        match = regex_pattern.search(request.text)
        if match is None:
            return None
        if verbose:
            print match.group()
        return BASE_URL + match.group()

    def get_materias(self, codigo, verbose=False):
        """
            Faz scraping da pagina do curriculo de um curso pegando nome e codigo
            de todas as materias

            Params:
                codigo - Codigo do curso
            Return:
                lista contendo tuplas de todas as materias no formato (Codigo da materia, nome)
                None em caso de erro
        """
        all_materias = []
        url = self.get_curriculo_url(codigo)
        if url is None:
            return None
        request = self.make_request(url)
        if request is None:
            return None
        soup = bs4.BeautifulSoup(request.text, 'html.parser')

        for link in soup.find_all('a'):
            if len(link.getText()) > 0 and link.getText()[0].isdigit():
                if verbose:
                    print link.getText()
                all_materias.append((link.getText()[:6], link.getText()[8:].strip()))

        if verbose:
            print 'LISTA DE MATERIAS:'
            pprint.pprint(all_materias)

        return all_materias



    def get_oferta(self, codigo):
        """
            Retorna todas as turmas de uma materia
        """
        request = self.make_request(BASE_OFERTA + str(codigo))
        if request is None:
            return None
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        data_div = soup.find_all('div')
        data_td = soup.find_all('td')

        turmas = get_info_turmas(data_div, data_td)

        return turmas

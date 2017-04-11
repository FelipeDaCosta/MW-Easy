# Author : Felipe da Costa Malaquias

"""
Contem as classes responsaveis por guardar os dados dos cursos, materias e turmas
"""
from Turma import Turma

class Materia(object):
    """
        Classe responsavel por guardar as informacoes de uma materia
    """
    def __init__(self, nome, codigo, scraper):
        self.scraper = scraper
        self.nome = nome
        self.codigo = codigo
        self.turmas = []
        self.get_oferta()

    def get_oferta(self):
        """
            Atualiza a oferta da materia no matricula web
        """
        new_oferta = self.scraper.get_oferta(self.codigo)
        if new_oferta != None:
            self.turmas = new_oferta
        else:
            self.turmas = []

    def add_turma(self, turma):
        """
            Adiciona uma turma ou lista de turmas para a materia
        """
        if isinstance(turma, list):
            self.turmas.extend(turma)
        elif isinstance(turma, Turma):
            self.turmas.append(turma)

    def print_oferta(self):
        """
            Imprime a oferta da materia
        """
        if self.turmas != None and self.turmas != []:
            for turma in self.turmas:
                turma.print_info()
                print '\n'
        else:
            print "Erro self.turmas == None"

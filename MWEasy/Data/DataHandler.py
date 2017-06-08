"""
Atualiza e mantem o banco de dados das materias
Banco: 
Personal Info: 
"""

import cPickle
import os
import Scraper
from Materia import Turma, Materia

# Constants
DICT_FILE = "data.mw"


class DataHandler(object):
    """
        Cria o banco de dados e faz a manutencao
    """
    def __init__(self):
        self.scraper = Scraper.Scraper()
        self.materias = {}       # Dicionario: Codigo_materia->Materia_obj
        self.nomes_materias = {} # Dicionario: Codigo_materia->nome_materia
        self.curso_materias = {} # Dicionario: Codigo_curso->lista_materias_do_curso (Ordem alfabetica)
        self.lista_cursos = []   # Lista com o nome de todos os cursos. Guardados em tuplas (cod, nome)
        if os.path.exists(DICT_FILE):
            with open(DICT_FILE, "rb") as f:
                self.materias, self.nomes_materias, self.curso_materias, self.lista_cursos = cPickle.load(f)


    def close(self):
        """
            Deve ser chamada ao final do programa para guardar as atualizacoes nos dicionarios.
        """
        with open(DICT_FILE, "wb") as f:
            cPickle.dump([self.materias, self.nomes_materias, self.curso_materias, self.lista_cursos], f)

    def get_lista_cursos(self):
        """
            Return:
                Retorna lista contendo tuplas (Codigo_curso, nome_curso) 
        """
        if not self.lista_cursos:
            self.lista_cursos = self.scraper.get_all_cursos()
        return self.lista_cursos
        
    def add_materias_from_curso(self, codigo):
        """
            Adiciona as materias do curso cujo codigo for passado.
            Codigo pode ser passado como str ou int.
            Nao cria o objeto materia, apenas adiciona o codigo e o nome no db
        """
        materias = self.scraper.get_materias(codigo)
        self.curso_materias[codigo] = materias
        for i in materias:
            if not self.materias.has_key(i[0]):
                self.materias[i[0]] = None
            if not self.nomes_materias.has_key(i[0]):
                self.nomes_materias[i[0]] = i[1]


    def get_materia(self, codigo):
        """
            Recebe o codigo de uma materia e busca no db. Se n encontrarar busca online e guarda no db

            Returns:
                objeto Materia referente ao codigo passado
                None caso o codigo nao esteja no db
        """
        if self.materias.has_key(codigo) and self.materias[codigo] is not None:
            return self.materias[codigo]

        new_materia = Materia(self.nomes_materias[codigo], codigo)
        new_materia.add_turmas(self.scraper.get_oferta(codigo))
        self.materias[codigo] = new_materia
        return new_materia

    def get_materias_from_curso(self, codigo):
        """
            Recebe o codigo de um curso e retorna uma lsita com todas as materias do curso

            Return:
                obj Materia do curso.
        """
        if self.curso_materias.has_key(codigo):
            return self.curso_materias[codigo]

        self.add_materias_from_curso(codigo)
        return self.curso_materias[codigo]



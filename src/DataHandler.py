"""
Atualiza e mantem o banco de dados das materias
"""

import cPickle
import os
import Spiders
import Materia

# Constants
DICT_FILE = os.path.join("..", "data", "data_dict.mw")
LIST_FILE = os.path.join("..", "data", "data_list.mw")



class DataHandler(object):
    """
    Cria o banco de dados e faz a manutencao
    """
    def __init__(self, curso):
        self.spider = Spiders.Spider()
        self.curso = curso

    def update_materias_curso(self, verbose=False):
        """
        Faz o update das informacoes de todas as materias do curso
        """
        materias = self.spider.get_materias(self.curso)
        if materias is None: # Codigo de curso valido
            return None

        lista_final_materias = []
        for mat in materias:
            materia = Materia.Materia(mat[1], mat[0], self.spider)
            if verbose:
                print materia.nome
            lista_final_materias.append(materia)

        self.store_data(lista_final_materias)
        return lista_final_materias

    def read_list(self):
        """
        Le o arquivo read_list.mw e retorna a lista. Retorna None caso o arquivo n exista
        """
        if os.path.isfile(LIST_FILE):
            list_file = cPickle.load(open(LIST_FILE, "rb"))
            return list_file
        return None

    def read_dict(self):
        """
        Le o arquivo data_dict.mw e retorna o dicionario. Retorna None caso o arquivo n exista
        """
        if os.path.isfile(DICT_FILE):
            dict_file = cPickle.load(open(DICT_FILE, "rb"))
            return dict_file
        return None

    def store_data(self, data):
        """
        Guarda os novos dados na lista (Para manter ordem) e no dicionario (busca)
        data deve ser do tipo lista
        """
        if not isinstance(data, list):
            return None
        dicionario_final_materias = dict((i.codigo, i) for i in data)
        if os.path.isfile(DICT_FILE):
            dict_file = self.read_dict()
            dict_file.update(dicionario_final_materias)
        else:
            cPickle.dump(dicionario_final_materias, open(DICT_FILE, "wb"))

        if os.path.isfile(LIST_FILE):
            lista_final_materias = self.read_list()
            # Juntando listas sem duplicates
            lista_final_materias.extend([x for x in data if x not in lista_final_materias])
            cPickle.dump(lista_final_materias, open(LIST_FILE, "wb"))
        else:
            cPickle.dump(data, open(LIST_FILE, "wb"))

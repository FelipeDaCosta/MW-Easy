# Author : Felipe da Costa Malaquias

"""
    Contem as classes responsaveis por guardar os dados dos cursos, materias e turmas
"""

class Turma(object):
    """
        Contem as informacoes das turmas como total de vagas, nome do professor e horarios.
    """
    def __init__(self, turma):
        self.turma = turma
        self.professor = None
        self.vagas = None
        self.horarios = []
        self.campus = None

    def horario_to_dict_str(self):
        """
            Experimental. Retorna a chave do dicionario de materias
        """
        final_str = ''
        for hora in self.horarios:
            horario = hora.split()
            final_str += (horario[0][:3]) + horario[1] + horario[2]
        return final_str

    def print_info(self):
        """
            Imprime todas as informacoes ja obtidas da turma
        """
        print 'Turma: ' + self.turma
        if self.campus != None:
            print 'Campus: ' + self.campus

        if self.professor != None:
            print 'Professor: ' + self.professor
        if self.vagas != None:
            print 'Vagas Restantes:', self.vagas
        if self.horarios != None:
            print 'Horarios: '
            for horarios in self.horarios:
                print horarios
            print self.horario_to_dict_str()
            print

    def set_turma(self, turma):
        """
            Seta a turma
        """
        self.turma = turma

    def set_professor(self, professor):
        """
            Seta o professor
        """
        self.professor = professor

    def set_vagas(self, vagas):
        """
            Seta os numeros de vagas
        """
        self.vagas = vagas


    def set_horarios(self, horarios):
        """
            Adiciona horarios a lista de horarios
        """
        self.horarios.append(horarios)

    def set_campus(self, campus):
        """
            Seta o campus
        """
        self.campus = campus

class Materia(object):
    """
        Classe responsavel por guardar as informacoes de uma materia
    """
    def __init__(self, nome, codigo):
        self.nome = nome
        self.codigo = codigo
        self.turmas = []

    def add_turmas(self, novas_turmas):
        """
            Adiciona novas turmas na lista
        """
        self.turmas.extend(novas_turmas)

    def get_turmas(self):
        """
            Retorna lista de turmas
        """
        return self.turmas

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

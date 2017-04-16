
"""
    Author: Felipe da Costa Malaquias
    Classe responsavel por carregar as informacoes das turmas
    como total de vagas disponiveis e ocupadas
    horarios e nome do(s) professor(es)
"""

class Turma(object):
    """
        Contem as informacoes das turmas
    """
    def __init__(self, turma=None, professor=None, vagas_str=None, horarios=None):
        self.turma = turma
        self.professor = professor
        self.vagas_str = vagas_str
        self.vagas_total = None
        self.vagas_ocupadas = None
        self.vagas_restantes = None
        self.calouros_vagas_total = None
        self.calouros_vagas_ocupadas = None
        self.calouros_vagas_restantes = None
        self.horarios = []
        if horarios != None:
            self.set_horarios(horarios)
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
        if self.turma != None:
            print 'Turma: ' + self.turma
        if self.campus != None:
            print 'Campus: ' + self.campus

        if self.professor != None:
            print 'Professor: ' + self.professor
        if self.vagas_str != None:
            print 'Vagas Total:    ', self.vagas_total
            print 'Vagas Ocupadas: ', self.vagas_ocupadas
            print 'Vagas Restantes:', self.vagas_restantes
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
        self.vagas_str = vagas
        lista_vagas = self.vagas_str.split()
        self.vagas_total = int(filter(unicode.isdigit, lista_vagas[0]))
        self.vagas_ocupadas = int(filter(unicode.isdigit, lista_vagas[1]))
        self.vagas_restantes = int(filter(unicode.isdigit, lista_vagas[2]))
        if len(lista_vagas) == 6:
            self.calouros_vagas_total = int(filter(unicode.isdigit, lista_vagas[3]))
            self.calouros_vagas_ocupadas = int(filter(unicode.isdigit, lista_vagas[4]))
            self.calouros_vagas_restantes = int(filter(unicode.isdigit, lista_vagas[5]))


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

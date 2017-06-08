import Tkinter as tk
import ttk
import sys
import threading
from Data import DataHandler as dh
from Grade import Cell, Table


class Lista_materias(tk.Listbox, object):
    """
    Classe da lista de materias que fica do lado esquerdo (<) da GUI
    """
    def __init__(self, parent, lista_materias):
        super(Lista_materias, self).__init__(parent)
        self.config(width=30)
        self.populate(lista_materias)
        self.grid(sticky=tk.E + tk.W + tk.S + tk.N)

    def populate(self, materias):
        """
        Recebe uma lista e popula a listbox com o elemento da lista
        """
        if materias is not None:
            for i, mat in enumerate(materias):
                self.insert(i, mat[1])

class Dropdown_menu(ttk.LabelFrame, object):
    """
    Classe do drop_down_menu. Consiste em um LabelFrame junto de um combobox
    """
    def __init__(self, parent, text, values):
        super(Dropdown_menu, self).__init__(parent, text=text)
        self.combobox = ttk.Combobox(self, values=values)
        self.grid()
        self.combobox.pack()

    def get_value(self):
        return self.combobox.get()

    def set_value(self, values):
        self.combobox.set(values)


class Filter(tk.Frame, object):
    """
    Class do filtro. Basicamente uma frame com varios checkbuttons que
    filtra a lista de materias
    """
    def __init__(self, parent):
        super(Filter, self).__init__(parent)
        self.checkBoxList = []
        self.varList = [] # Variaveis dos checkbox
        self.pack()

    def add_filter(self, text, onvalue):
        """
        Recebe o texto do checkbutton e os valores para onvalue e offvalue
        os valores devem ser strings pra ficar mais facil saber quais estao ligados
        onvalue nao pode ser "off"
        """
        if onvalue == "off":
            print "onvalue cannot be off. Checkbutton", text, "not added"
            return
        var = tk.StringVar()
        self.checkBoxList.append(tk.Checkbutton(self, text=text, onvalue=onvalue, offvalue="off", variable=var))
        self.varList.append(var)

    def pack_check_button(self):
        """
        Coloca os checkbuttons no frame
        """
        for checkBox in self.checkBoxList:
            checkBox.pack()

    def get_checks(self):
        """

        """
        checked = []
        for value in self.varList:
            if value.get() != "off":
                checked.append(value.get())
        return checked



class Main(tk.Frame, object):
    def __init__(self, parent, *args, **kwargs):
        self.data_handler = dh()
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame_materias = tk.Frame(self)
        self.frame_materias.rowconfigure(0, weight=1)
        self.list_box = Lista_materias(self.frame_materias, self.data_handler.get_materias_from_curso(35))
        self.frame_materias.grid(sticky=tk.W + tk.N + tk.S, row=0, rowspan=2)

        self.frame_label = tk.Frame(self)
        Dropdown_menu(self.frame_label, "Cursos", ["aaa", "bbb", "ccc"])
        self.frame_label.grid(row=1, column=3)
        """
        self.frame_table = tk.Frame(self)
        self.frame_table.columnconfigure(0, weight=1)
        teste = Table(self.frame_table)
        self.frame_table.grid(row=0, column=2, padx=10, pady=10, sticky=tk.E+tk.N+tk.W+tk.S, columnspan=3)
        """

        self.frame_table = tk.Frame(self)
        self.frame_table.columnconfigure(0, weight=1)
        Table(self.frame_table)
        self.frame_table.grid(row=0, column=2, padx=10, pady=10, sticky=tk.E+tk.N+tk.W+tk.S, columnspan=2)

        self.frame_filter = tk.Frame(self)
        filtros = Filter(self.frame_filter)
        filtros.add_filter("Testando", "Ligado")
        filtros.pack_check_button()
        self.frame_filter.grid(row=1, column=2)

        self.frame_button = tk.Frame(self)
        def print_check():
            print filtros.get_checks()
        but = tk.Button(self.frame_button, text="aa", command=print_check)
        but.pack()
        self.frame_button.grid(row=1, column=1)
        


        

    def dispose(self):
        self.data_handler.close()
        

if __name__ == "__main__":
    root = tk.Tk()
    main_frame = Main(root)
    main_frame.pack(side="top", fill="both", expand=True)

    def on_closing():
        main_frame.dispose()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

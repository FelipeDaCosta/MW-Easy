import Tkinter as tk
import sys
import threading
from Data import DataHandler as dh


class Lista_materias(tk.Listbox, object):
    """
    Classe da lista de materias que fica do lado direito (>) da GUI
    """
    def __init__(self, frame, lista_materias):
        super(Lista_materias, self).__init__(frame)
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

class Main(tk.Frame, object):
    def __init__(self, parent, *args, **kwargs):
        self.data_handler = dh()
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame_materias = tk.Frame(self)
        self.frame_materias.rowconfigure(0, weight=1)
        self.list_box = Lista_materias(self.frame_materias, self.data_handler.get_materias_from_curso(1341))
        self.frame_materias.grid(sticky=tk.W + tk.N + tk.S)

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

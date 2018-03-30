# Taken from https://github.com/dmnfarrell/pandastable/wiki/Code-Examples

from tkinter import *
from pandastable import Table, TableModel
from AppData.Scripts.funciones import base_datos as bd
import pandas as pd

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master

        self.main.geometry('600x400+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        base_datos = bd()
        base_datos.cargar_datos()
        pozo = "Allegheny"
        datos = base_datos.get_valores_pozo(pozo)
        df = pd.DataFrame(data=datos[1:][:],columns=datos[0][:])
        self.table = pt = Table(f, dataframe=df,showtoolbar=False, showstatusbar=False)
        pt.show()
        return

app = TestApp()
#launch the app
app.mainloop()
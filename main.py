import tkinter as tk
import numpy as np
import pandas as pd
from pandastable import Table

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        #top.rowconfigure(1, weight =1)
        top.columnconfigure(0, weight =1)
        top.columnconfigure(1, weight =1)
        self.createWidgets()


    def createWidgets(self):
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight =1)
        self.columnconfigure(0, weight =1)
        #self.columnconfigure(1, weight=1)
        array=np.array([[1,2],[3,4]])
        self.frame_tabla=tk.Frame(self)
        self.tabla=Table(self.frame_tabla,dataframe=pd.DataFrame(data=array),showstatusbar=False,showtoolbar=False)
        self.tabla.show()
        self.frame_tabla.grid(row=0,column=1,sticky=tk.W+tk.E+tk.S+tk.N)
        self.boton_consulta = tk.Button(self, text='Consultar Pozo', command=None)
        self.boton_consulta.grid(row=0,column=0,sticky=tk.W+tk.E+tk.S+tk.N)


app=Application()
app.master.title("PRUEBAS")
#app.master.resizable(0,0)
app.master.geometry("600x400+50+20")
app.mainloop()

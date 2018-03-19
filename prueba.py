import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from AppData.Scripts.funciones import base_datos as bd
from pandastable import Table

class Application(tk.Frame):
    def __init__(self,master=None):
        self.clase_base_de_datos = bd() #inicializo la clase de base de datos para manejar los datos
        self.data = self.clase_base_de_datos.cargar_datos() #Cargo los datos ya arreglados de la base de datos
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.rowconfigure(1, weight =1)
        top.columnconfigure(0, weight =1)
        top.columnconfigure(1, weight =1)
        self.createWidgets()


    def createWidgets(self):
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight =1)
        self.columnconfigure(0, weight =1)
        self.columnconfigure(1, weight=1)
        self.imagen_fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")
        self.fondo_pantalla=tk.Label(self,image=self.imagen_fondo)
        self.fondo_pantalla.grid(row=0,column=0,rowspan=2,columnspan=2,sticky=tk.S+tk.N+tk.W+tk.E)
        self.boton_consulta = tk.Button(self, text='Consultar Pozo', command=self.ventana_consulta)
        self.boton_consulta.grid(row=1,column=0,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)
        self.boton_analogia = tk.Button(self, text='Realizar Analogia', command=self.ventana_analogia)
        self.boton_analogia.grid(row=1,column=1,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)

    def ventana_consulta(self):
        self.consulta=tk.Toplevel()
        self.consulta.title("Consulta de Pozos existentes")
        self.consulta.geometry("400x45+50+20")
        self.consulta.resizable(0,0)
        self.consulta.grid()
        self.consulta.rowconfigure(0,weight=1)
        self.consulta.rowconfigure(1,weight=1)
        self.consulta.columnconfigure(0,weight=1)
        self.consulta.columnconfigure(1,weight=3)
        self.label_pozo=tk.Label(self.consulta,text="Seleccione un pozo:")
        self.lista_pozos=ttk.Combobox(self.consulta,state="readonly",values=self.clase_base_de_datos.get_pozos())
        self.boton_consultar=tk.Button(self.consulta,text="Consultar",command=self.resultado_consulta)
        self.label_pozo.grid(row=0,column=0)
        self.lista_pozos.grid(row=0,column=1,sticky=tk.E+tk.W)
        self.boton_consultar.grid(row=1,column=0,columnspan=2)

    def resultado_consulta(self):
        if(len(self.lista_pozos.get()) == 0):# or len(self.lista_categorias.get()) == 0):
            messagebox.showerror("Error en la consulta","Digite los datos faltantes para realizar la \n la consulta en la base de datos")
        else:
            pozo=self.lista_pozos.get()
            self.consulta.destroy()
            self.resultado = tk.Toplevel()
            self.resultado.title("Resultado de la consulta del pozo: "+ pozo)
            self.resultado.geometry("800x600+50+20")
            self.resultado.grid()
            busqueda=self.clase_base_de_datos.get_valores_pozo(pozo)
            busqueda_to_dataframe = pd.DataFrame(data=busqueda[1:][:],columns=busqueda[0][:])
            self.table = Table(self.resultado,dataframe=busqueda_to_dataframe,showstatusbar=False,showtoolbar=False) #Con este table puedo mostrar la tabla de consulta
            self.table.show()

    def ventana_analogia(self):
        self.analogia = tk.Toplevel()
        self.analogia.title("Modulo para realizar analogia de un nuevo pozo")
        self.analogia.geometry("800x600+50+20")
        self.analogia.resizable(0, 0)
        self.analogia.grid()
        for i in range(0, 11):
            self.analogia.rowconfigure(i, weight=1)
        for i in range(0, 6):
            self.analogia.columnconfigure(i, weight=1)
        self.nombre_pozo = tk.Label(self.analogia, text="Nombre del pozo:", bg="#fff", relief="groove")
        self.propiedades = tk.Label(self.analogia, text="Propiedades para analogia", bg="#fff", relief="groove")
        self.unidades = tk.Label(self.analogia, text="Unidades", bg="#fff", relief="groove")
        self.puntual = tk.Label(self.analogia, text="Valor puntual", bg="#fff", relief="groove")
        self.min = tk.Label(self.analogia, text="Valor minimo", bg="#fff", relief="groove")
        self.max = tk.Label(self.analogia, text="Valor maximo", bg="#fff", relief="groove")
        self.ponderacion = tk.Label(self.analogia, text="Ponderacion", bg="#fff", relief="groove")
        propi_unida = self.clase_base_de_datos.lista_propiedades_analogia() #Obtengo la matriz con las propiedades y unidades




app=Application()
app.master.title("SOFTWARE D.I.S")
app.master.resizable(0,0)
app.master.geometry("800x600+50+20")
app.mainloop()

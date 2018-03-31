import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
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
        #self.letra_titulos = tkFont.Font(family="Lucida Sans",size=8,weight="bold")
        #self.letra_botones = tkFont.Font(family="Lucida Sans",size=8,weight="normal")
        #self.letra_contenido = tkFont.Font(family="Lucida Sans",size=8,weight="normal")
        self.createWidgets()


    def createWidgets(self):
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight =1)
        self.columnconfigure(0, weight =1)
        self.columnconfigure(1, weight=1)
        self.imagen_fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")
        self.fondo_pantalla=tk.Label(self,image=self.imagen_fondo)
        self.fondo_pantalla.grid(row=0,column=0,rowspan=2,columnspan=2,sticky=tk.S+tk.N+tk.W+tk.E)
        self.boton_consulta = tk.Button(self, text='Consultar Pozo',command=self.ventana_consulta)
        self.boton_consulta.grid(row=1,column=0,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)
        self.boton_analogia = tk.Button(self, text='Realizar Analogia',command=self.ventana_analogia)
        self.boton_analogia.grid(row=1,column=1,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)

    def ventana_consulta(self):
        self.consulta=tk.Toplevel()
        self.consulta.title("Consulta de Pozos existentes")
        self.consulta.geometry("450x65+50+20")
        self.consulta.resizable(0,0)
        self.consulta.grid()
        self.consulta.config(bg="#fff")
        self.consulta.rowconfigure(0,weight=1)
        self.consulta.rowconfigure(1,weight=1)
        self.consulta.columnconfigure(0,weight=1)
        self.consulta.columnconfigure(1,weight=3)
        self.label_pozo=tk.Label(self.consulta,text="Seleccione un pozo:",bg="#fff")
        self.lista_pozos=ttk.Combobox(self.consulta,state="readonly",values=self.clase_base_de_datos.get_pozos())
        self.boton_consultar=tk.Button(self.consulta,text="Consultar",command=self.resultado_consulta)
        self.label_pozo.grid(row=0,column=0)
        self.lista_pozos.grid(row=0,column=1,sticky=tk.E+tk.W)
        self.boton_consultar.grid(row=1,column=0,columnspan=2)

    def resultado_consulta(self):
        if(len(self.lista_pozos.get()) == 0):# or len(self.lista_categorias.get()) == 0):
            messagebox.showerror("Error en la consulta","Digite los datos faltantes para realizar la \nla consulta en la base de datos")
        else:
            pozo=self.lista_pozos.get()
            self.consulta.destroy()
            self.resultado = tk.Toplevel()
            self.resultado.title("Resultado de la consulta del pozo: "+ pozo)
            self.resultado.geometry("800x600+50+20")
            self.resultado.grid()
            busqueda=np.asarray(self.clase_base_de_datos.get_valores_pozo(pozo))
            columna_unidades = []
            columna_valores = []
            columna_fecha = []
            for i in range(len(busqueda)):
                columna_unidades.append([busqueda[i, 2]])
                columna_valores.append([busqueda[i, 3]])
                columna_fecha.append([busqueda[i, 4]])
            busqueda = np.delete(busqueda, np.s_[2:5], axis=1)
            columna_unidades = np.asarray(columna_unidades)
            columna_valores = np.asarray(columna_valores)
            columna_fecha = np.asarray(columna_fecha)
            busqueda = np.append(busqueda, columna_valores, axis=1)
            busqueda = np.append(busqueda, columna_unidades, axis=1)
            busqueda = np.append(busqueda, columna_fecha, axis=1)
            busqueda_to_dataframe = pd.DataFrame(data=busqueda[1:,:],columns=busqueda[0,:])
            self.table = Table(self.resultado,dataframe=busqueda_to_dataframe,showstatusbar=False,showtoolbar=False) #Con este table puedo mostrar la tabla de consulta
            self.table.show()

    def ventana_analogia(self):
        self.analogia = tk.Toplevel()
        self.analogia.title("Modulo para realizar analogia de un nuevo pozo")
        self.analogia.geometry("800x600+50+20")
        self.analogia.config(bg="#fff")
        self.analogia.grid()
        for i in range(0, 11):
            self.analogia.rowconfigure(i, weight=1)
        for i in range(0, 6):
            self.analogia.columnconfigure(i, weight=1)
        self.nombre_pozo = tk.Label(self.analogia, text="Nombre del pozo:", bg="#fff", relief="groove")
        self.campo_nombre_pozo  = tk.Entry(self.analogia,bg="#fff",relief="groove")
        self.propiedades = tk.Label(self.analogia, text="Propiedades para analogia", bg="#fff", relief="groove")
        self.unidades = tk.Label(self.analogia, text="Unidades", bg="#fff", relief="groove")
        self.puntual = tk.Label(self.analogia, text="Valor único", bg="#fff", relief="groove")
        self.min = tk.Label(self.analogia, text="Valor minimo", bg="#fff", relief="groove")
        self.max = tk.Label(self.analogia, text="Valor maximo", bg="#fff", relief="groove")
        self.ponderacion = tk.Label(self.analogia, text="Ponderacion", bg="#fff", relief="groove")
        self.nombre_pozo.grid(row=0, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.campo_nombre_pozo.grid(row=0, column=3, columnspan=3, sticky=tk.N + tk.S + tk.W + tk.E)
        self.propiedades.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.unidades.grid(row=1, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        self.puntual.grid(row=1, column=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.min.grid(row=1, column=3, sticky=tk.N + tk.S + tk.W + tk.E)
        self.max.grid(row=1, column=4, sticky=tk.N + tk.S + tk.W + tk.E)
        self.ponderacion.grid(row=1, column=5, sticky=tk.N + tk.S + tk.W + tk.E)
        propi_unida = self.clase_base_de_datos.lista_propiedades_analogia() #Obtengo la matriz con las propiedades y unidades
        for i in range(0,len(propi_unida[0])):
            propiedad = tk.Label(self.analogia,text=propi_unida[0][i],bg="#fff",relief="groove")
            unidades = tk.Label(self.analogia,text=propi_unida[1][i],bg="#fff",relief="groove")
            propiedad.grid(row=2+i,column=0,sticky=tk.N + tk.S + tk.W + tk.E)
            unidades.grid(row=2+i,column=1,sticky=tk.N + tk.S + tk.W + tk.E)
        self.matrix_valores=[]
        for j in range(0,4):
            columna=[]
            for i in range(0,8):
                valor_ingresar = tk.Entry(self.analogia,bg="#fff",justify=tk.CENTER,relief="groove")
                valor_ingresar.grid(row=2+i, column=2+j, sticky=tk.N + tk.S + tk.W + tk.E)
                columna.append(valor_ingresar)
            self.matrix_valores.append(columna)
        self.boton_ponderado = tk.Button(self.analogia,text="Establecer Ponderaciones",command=self.set_ponderaciones)
        self.boton_analogia_promedio = tk.Button(self.analogia,text="Realizar Analogia por Valor Promedio",command=self.calculo_analogia_promedio)
        self.boton_analogia_jaccard = tk.Button(self.analogia,text="Realizar Analogia por Jaccard",command=self.calculo_analogia_jaccard)
        self.boton_ponderado.grid(row=10,column=0,columnspan=2)
        self.boton_analogia_promedio.grid(row=10,column=2,columnspan=2)
        self.boton_analogia_jaccard.grid(row=10,column=4,columnspan=2)

    def set_ponderaciones(self):
        columnas_llenar=[]
        for i in range(0,len(self.matrix_valores[3])):
            self.matrix_valores[3][i].delete(0, tk.END)
            if(len(self.matrix_valores[0][i].get())!=0 or (len(self.matrix_valores[1][i].get())!=0 and len(self.matrix_valores[2][i].get())!=0)):
                columnas_llenar.append(self.matrix_valores[3][i])
        for i in columnas_llenar:
            i.insert(0,str(100*1.0/len(columnas_llenar)))

    def resultado_analogia_promedio(self):
        pass

    def resultado_analogia_jaccard(self):
        pass

    def calculo_analogia_promedio(self):
        filas_llenadas,valor_puntual,flag = self.comprobar_filas_llenadas()
        if flag:
            matrix_comparar=self.generacion_matrix_nuevo_pozo(filas_llenadas,valor_puntual)
        else:
            messagebox.showerror("Error en la analogia",
                                 "Digite correctamente los datos para realizar la \nla analogia del pozo digitado")

    def calculo_analogia_jaccard(self):
        filas_llenadas,valor_puntual, flag = self.comprobar_filas_llenadas()
        if flag:
            matrix_comparar = self.generacion_matrix_nuevo_pozo(filas_llenadas, valor_puntual)
        else:
            messagebox.showerror("Error en la analogia",
                                 "Digite correctamente los datos para realizar la \nla analogia del pozo digitado")

    def comprobar_filas_llenadas(self):
        filas_llenadas = [] #En este vector se guarda los indices de las filas que se han llenado en los entry's
        valor_puntual=[] #En este vector se guarda la informacion si corresponde a un valor puntual o un rango
        if (len(self.campo_nombre_pozo.get())!=0):
            for i in range(0, len(self.matrix_valores[0])):
                if (len(self.matrix_valores[0][i].get()) != 0 and (
                        len(self.matrix_valores[1][i].get()) == 0 and len(self.matrix_valores[2][i].get()) == 0) and len(
                        self.matrix_valores[3][i].get()) != 0):
                    filas_llenadas.append(i)
                    valor_puntual.append(True)
                elif (len(self.matrix_valores[0][i].get()) == 0 and (
                        len(self.matrix_valores[1][i].get()) != 0 and len(self.matrix_valores[2][i].get()) != 0) and len(
                        self.matrix_valores[3][i].get()) != 0):
                    filas_llenadas.append(i)
                    valor_puntual.append(False)
                elif (len(self.matrix_valores[0][i].get()) == 0 and (
                        len(self.matrix_valores[1][i].get()) == 0 and len(self.matrix_valores[2][i].get()) == 0) and len(
                        self.matrix_valores[3][i].get()) == 0):
                    pass
                else:
                    filas_llenadas.append('error')
            if filas_llenadas == [] or 'error' in filas_llenadas:
                return filas_llenadas, valor_puntual, False
            else:
                return filas_llenadas, valor_puntual, True
        else:
            return filas_llenadas, valor_puntual, False

    def generacion_matrix_nuevo_pozo(self,filas_llenadas,valor_puntual):
        matrix_comparar = []
        for i in range(1 + len(filas_llenadas)):
            fila = []
            for j in range(2):
                if (j == 0 and i == 0):
                    fila.append('Pozo')
                elif (i == 0 and j != 0):
                    fila.append(self.campo_nombre_pozo.get())
                elif (j == 0 and i != 0):
                    fila.append(self.clase_base_de_datos.lista_propiedades_analogia()[0][filas_llenadas[i - 1]])
                else:
                    if (valor_puntual[i - 1]):
                        fila.append(float(self.matrix_valores[0][i-1].get()))
                    else:
                        fila.append([float(k) for k in range(int(self.matrix_valores[1][i-1].get()),int(self.matrix_valores[2][i-1].get())+1)])
            matrix_comparar.append(fila)
        return matrix_comparar

app=Application()
app.master.title("SOFTWARE D.I.S")
app.master.resizable(0,0)
app.master.geometry("800x600+50+20")
app.mainloop()

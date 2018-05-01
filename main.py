import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
from AppData.Scripts.funciones import base_datos as bd
from pandastable import Table
import tkinter.font as tkFont

class Application(tk.Frame):
    def __init__(self,master=None):
        self.clase_base_de_datos = bd() #inicializo la clase de base de datos para manejar los datos
        self.clase_base_de_datos.cargar_datos() #Cargo los datos ya arreglados de la base de datos
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.rowconfigure(1, weight =1)
        top.columnconfigure(0, weight =1)
        self.letra = tkFont.Font(family="Lucida Sans",size=12,weight="normal")
        self.createWidgets()

    def createWidgets(self): #Ventana principal
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight =1)
        self.columnconfigure(0, weight =1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.imagen_fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")
        self.fondo_pantalla=tk.Label(self,image=self.imagen_fondo)
        self.fondo_pantalla.grid(row=0,column=0,rowspan=2,columnspan=3,sticky=tk.S+tk.N+tk.W+tk.E)
        self.boton_consulta = tk.Button(self, text='Agregar Campo', command=self.ventana_nuevo_pozo)
        self.boton_consulta.grid(row=1, column=0, padx=80, pady=100, sticky=tk.W + tk.E + tk.S)
        self.boton_consulta = tk.Button(self, text='Consultar Campo',command=self.ventana_consulta)
        self.boton_consulta.grid(row=1,column=1,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)
        self.boton_analogia = tk.Button(self, text='Realizar Analogia',command=self.ventana_analogia)
        self.boton_analogia.grid(row=1,column=2,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)

    def ventana_nuevo_pozo(self):
        self.nuevo_pozo=tk.Toplevel()
        self.nuevo_pozo.title("Agregacion de nuevo campo")
        self.nuevo_pozo.geometry("800x600+100+80")
        self.nuevo_pozo.config(bg="#fff")
        self.nuevo_pozo.grid()
        self.nuevo_pozo.rowconfigure(0, weight=1)
        self.nuevo_pozo.rowconfigure(1, weight=3)
        self.nuevo_pozo.rowconfigure(2, weight=1)
        self.nuevo_pozo.columnconfigure(0, weight=1)
        self.nuevo_pozo.columnconfigure(1, weight=1)
        label_nuevo_pozo=tk.Label(self.nuevo_pozo,text="Nombre del nuevo campo:",bg="#fff",relief="groove")
        self.entry_nuevo_pozo=tk.Entry(self.nuevo_pozo,justify=tk.CENTER)
        frame_tabla=tk.Frame(self.nuevo_pozo)
        boton_agregar=tk.Button(self.nuevo_pozo,text="Agregar nuevo campo",command=self.agregar_nuevo_campo)
        matrix_nuevo_campo=np.asarray(self.clase_base_de_datos.get_propiedades_unidades())
        matrix_dataframe=pd.DataFrame(data=matrix_nuevo_campo[1:,:],columns=matrix_nuevo_campo[0,:])
        self.tabla_nuevo_campo=Table(frame_tabla,dataframe=matrix_dataframe,showstatusbar=False,showtoolbar=False)
        self.tabla_nuevo_campo.show()
        label_nuevo_pozo.grid(row=0,column=0,sticky=tk.E+tk.W, ipady=15)
        self.entry_nuevo_pozo.grid(row=0,column=1,sticky=tk.E+tk.W, ipady=15)
        frame_tabla.grid(row=1,column=0,columnspan=2,sticky=tk.N+tk.S+tk.E+tk.W)
        boton_agregar.grid(row=2,column=0,columnspan=2, ipadx=50, ipady=10)

    def agregar_nuevo_campo(self): #Funcion que ejecuta el comando para agregar un nuevo campo
        if (len(self.entry_nuevo_pozo.get()) == 0):
            messagebox.showerror("Error en los datos",
                                 "Digite los datos faltantes para agregar el \nnuevo campo.",
                                 parent=self.nuevo_pozo)
        else:
            self.tabla_nuevo_campo.setSelectedCells(0,self.tabla_nuevo_campo.rows,0,self.tabla_nuevo_campo.cols)
            datos=self.tabla_nuevo_campo.getSelectedDataFrame().values
            if(datos[0,0]!=self.clase_base_de_datos.datos.at[2,1]):
                self.clase_base_de_datos.agregar_campo_nuevo(self.entry_nuevo_pozo.get(),datos[1:,2:])
                messagebox.showinfo("Operacion exitosa", "Se ha agrega el nuevo campo \n exitosamente", parent=self.nuevo_pozo)
                self.nuevo_pozo.destroy()
            else:
                messagebox.showerror("Error en los datos",
                                     "Digite los datos faltantes para agregar el \nnuevo campo.",
                                     parent=self.nuevo_pozo)

    def ventana_consulta(self): #Ventana para realizar la consulta pidiendo el campo
        self.consulta=tk.Toplevel()
        self.consulta.title("Consulta de Campos existentes")
        self.consulta.geometry("450x65+100+80")
        self.consulta.resizable(0,0)
        self.consulta.grid()
        self.consulta.config(bg="#fff")
        self.consulta.rowconfigure(0,weight=1)
        self.consulta.rowconfigure(1,weight=1)
        self.consulta.columnconfigure(0,weight=1)
        self.consulta.columnconfigure(1,weight=3)
        self.label_pozo=tk.Label(self.consulta,text="Seleccione un campo:",bg="#fff")
        self.lista_pozos=ttk.Combobox(self.consulta,state="readonly",values=self.clase_base_de_datos.get_pozos())
        self.boton_consultar=tk.Button(self.consulta,text="Consultar",command=self.resultado_consulta)
        self.label_pozo.grid(row=0,column=0)
        self.lista_pozos.grid(row=0,column=1,sticky=tk.E+tk.W)
        self.boton_consultar.grid(row=1,column=0,columnspan=2)

    def ordenar_datos_mostrar_tabla(self,matrix): #Funcion para ordenar los datos a mostrar en el resultado de la consulta
        matrix=np.asarray(matrix)
        columna_unidades = []
        columna_valores = []
        columna_fecha = []
        for i in range(len(matrix)):
            columna_unidades.append([matrix[i, 2]])
            columna_valores.append([matrix[i, 3]])
            columna_fecha.append([matrix[i, 4]])
        matrix = np.delete(matrix, np.s_[2:5], axis=1)
        columna_unidades = np.asarray(columna_unidades)
        columna_valores = np.asarray(columna_valores)
        columna_fecha = np.asarray(columna_fecha)
        matrix = np.append(matrix, columna_valores, axis=1)
        matrix= np.append(matrix, columna_unidades, axis=1)
        matrix = np.append(matrix, columna_fecha, axis=1)
        return matrix

    def desordenar_datos_mostrar_tabla(self,matrix): #Funcion que deshace el orden al mostrar los datos para actualizar los datos
        matrix=np.asarray(matrix)
        columna_unidades = []
        columna_valores = []
        columna_fecha = []
        for i in range(len(matrix)):
            columna_unidades.append([matrix[i, 3]])
            columna_valores.append([matrix[i, 2]])
            columna_fecha.append([matrix[i, 4]])
        matrix = np.delete(matrix, np.s_[2:5], axis=1)
        columna_unidades = np.asarray(columna_unidades)
        columna_valores = np.asarray(columna_valores)
        columna_fecha = np.asarray(columna_fecha)
        matrix = np.append(matrix, columna_unidades, axis=1)
        matrix = np.append(matrix, columna_valores, axis=1)
        matrix = np.append(matrix, columna_fecha, axis=1)
        return matrix

    def resultado_consulta(self): #Ventana que muestra el resultado de la consulta de ese campo
        if(len(self.lista_pozos.get()) == 0):# or len(self.lista_categorias.get()) == 0):
            messagebox.showerror("Error en la consulta","Digite los datos faltantes para realizar la \nla consulta en la base de datos",parent=self.consulta)
        else:
            self.pozo=self.lista_pozos.get()
            self.consulta.destroy()
            self.resultado = tk.Toplevel()
            self.resultado.title("Resultado de la consulta del campo: "+ self.pozo)
            self.resultado.geometry("800x600+50+20")
            self.resultado.grid()
            self.resultado.rowconfigure(0,weight=9)
            self.resultado.rowconfigure(1,weight=1)
            self.resultado.columnconfigure(0,weight=1)
            self.resultado.columnconfigure(1, weight=1)
            self.frame_tabla_consulta=tk.Frame(self.resultado)
            busqueda=self.ordenar_datos_mostrar_tabla(self.clase_base_de_datos.get_valores_pozo(self.pozo))
            self.busqueda_to_dataframe = pd.DataFrame(data=busqueda[1:,:],columns=busqueda[0,:])
            self.table = Table(self.frame_tabla_consulta,dataframe=self.busqueda_to_dataframe,showstatusbar=False,showtoolbar=False) #Con este table puedo mostrar la tabla de consulta
            self.table.show()
            self.frame_tabla_consulta.grid(row=0,column=0,columnspan=2,sticky=tk.N+tk.S+tk.W+tk.E)
            self.boton_exportar_excel_consulta=tk.Button(self.resultado,text="Exportar a Excel",command=self.ventana_guardar_excel_consulta)
            self.boton_exportar_excel_consulta.grid(row=1,column=0,ipadx=50,ipady=10)
            self.boton_actualizar = tk.Button(self.resultado, text="Actualizar Datos",command=self.actualizar_datos)
            self.boton_actualizar.grid(row=1, column=1, ipadx=50, ipady=10)

    def actualizar_datos(self):
        self.table.setSelectedCells(0,self.table.rows,0,self.table.cols)
        datos=self.table.getSelectedDataFrame().values
        if(datos[0,0]!=self.clase_base_de_datos.datos.at[2,0]):
            datos=self.desordenar_datos_mostrar_tabla(datos[1:,1:])
        else:
            datos = self.desordenar_datos_mostrar_tabla(datos)
        self.clase_base_de_datos.set_valores_pozo(datos[:,2:],self.pozo)
        messagebox.showinfo("Operacion exitosa", "Se ha actualizado el campo \n exitosamente", parent=self.resultado)
        self.resultado.destroy()

    def ventana_analogia(self): #Ventana para realizar el modulo de una analogia
        self.analogia = tk.Toplevel()
        self.analogia.title("Modulo para realizar analogia de un nuevo campo")
        self.analogia.geometry("1250x325+70+30")
        self.analogia.config(bg="#fff")
        self.analogia.grid()
        for i in range(0, 11):
            self.analogia.rowconfigure(i, weight=1)
        for i in range(0, 6):
            self.analogia.columnconfigure(i, weight=1)
        self.nombre_pozo = tk.Label(self.analogia, text="Nombre del campo:", bg="#E8F06B", relief="groove",font=self.letra)
        self.campo_nombre_pozo  = tk.Entry(self.analogia,bg="#E2EBC8",relief="groove",justify=tk.CENTER,font=self.letra)
        self.propiedades = tk.Label(self.analogia, text="Propiedades para analogia", bg="#E8F06B", relief="groove",font=self.letra)
        self.unidades = tk.Label(self.analogia, text="Unidades", bg="#E8F06B", relief="groove",font=self.letra)
        self.puntual = tk.Label(self.analogia, text="Valor único", bg="#E8F06B", relief="groove",font=self.letra)
        self.min = tk.Label(self.analogia, text="Valor minimo", bg="#E8F06B", relief="groove",font=self.letra)
        self.max = tk.Label(self.analogia, text="Valor maximo", bg="#E8F06B", relief="groove",font=self.letra)
        self.ponderacion = tk.Label(self.analogia, text="Ponderacion(%)", bg="#E8F06B", relief="groove",font=self.letra)
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
            propiedad = tk.Label(self.analogia,text=propi_unida[0][i],bg="#76F072",relief="groove",font=self.letra)
            unidades = tk.Label(self.analogia,text=propi_unida[1][i],bg="#76F072",relief="groove",font=self.letra)
            propiedad.grid(row=2+i,column=0,sticky=tk.N + tk.S + tk.W + tk.E)
            unidades.grid(row=2+i,column=1,sticky=tk.N + tk.S + tk.W + tk.E)
        self.matrix_valores=[]
        for j in range(0,4):
            columna=[]
            for i in range(0,8):
                valor_ingresar = tk.Entry(self.analogia,bg="#E2EBC8",justify=tk.CENTER,relief="groove",font=self.letra)
                valor_ingresar.grid(row=2+i, column=2+j, sticky=tk.N + tk.S + tk.W + tk.E)
                columna.append(valor_ingresar)
            self.matrix_valores.append(columna)
        self.boton_ponderado = tk.Button(self.analogia,text="Establecer Ponderaciones",command=self.set_ponderaciones,font=self.letra)
        self.boton_analogia_promedio = tk.Button(self.analogia,text="Realizar Analogia por Valor Promedio",command=self.resultado_analogia_promedio,font=self.letra)
        self.boton_analogia_jaccard = tk.Button(self.analogia,text="Realizar Analogia por Jaccard",command=self.resultado_analogia_jaccard,font=self.letra)
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
        self.resultados,self.valores_nuevo_pozo,self.datos_pozos=self.calculo_analogia_promedio()
        matrix_mostrar=[]
        for i in range(len(self.datos_pozos[0])+1):
            fila=[]
            for j in range(len(self.datos_pozos)+1):
                if(j==0 and i==0):
                    fila.append('Puntaje(%)')
                elif(i==0 and j==1):
                    fila.append('Campo')
                elif(i==0 and j not in [0,1]):
                    fila.append(self.clase_base_de_datos.lista_propiedades_unidades(self.valores_nuevo_pozo[j-1][i]))
                elif(i!=0 and j==0):
                    if(i!=1):
                        fila.append(str(self.get_valor_resultado(self.resultados,self.datos_pozos[j][i-1])))
                    else:
                        fila.append('100.0')
                elif(i!=0 and j==1):
                    if(i==1):
                        fila.append(self.valores_nuevo_pozo[0][i])
                    else:
                        fila.append(self.datos_pozos[0][i-1])
                else:
                    if(i==1):
                        fila.append(self.get_valor_to_string(self.valores_nuevo_pozo[j-1][i]))
                    else:
                        fila.append(self.get_valor_to_string(self.datos_pozos[j-1][i-1]))
            matrix_mostrar.append(fila)
        self.analogia.destroy()
        self.resultado_analogia=tk.Toplevel()
        self.resultado_analogia.title("Resultado de la analogia del campo: " + self.valores_nuevo_pozo[0][1])
        self.resultado_analogia.geometry("525x290+50+20")
        self.resultado_analogia.grid()
        self.resultado_analogia.rowconfigure(0,weight=9)
        self.resultado_analogia.rowconfigure(1,weight=1)
        self.resultado_analogia.columnconfigure(0,weight=1)
        self.resultado_analogia.columnconfigure(1,weight=1)
        self.frame_tabla_analogia=tk.Frame(self.resultado_analogia)
        matrix_mostrar=np.asarray(matrix_mostrar)
        self.df_matrix=pd.DataFrame(data=matrix_mostrar[1:,:],columns=matrix_mostrar[0,:])
        self.df_matrix = self.df_matrix.reindex(index=self.ordenar_dataframe())
        self.tabla_analogia=Table(self.frame_tabla_analogia,dataframe=self.df_matrix,showstatusbar=False,showtoolbar=False)
        self.tabla_analogia.show()
        self.frame_tabla_analogia.grid(row=0,column=0,columnspan=2,sticky=tk.N+tk.S+tk.W+tk.E)
        self.boton_exportar_excel_analogia = tk.Button(self.resultado_analogia, text="Exportar a Excel", command=self.ventana_guardar_excel_analogia)
        self.boton_exportar_excel_analogia.grid(row=1, column=0, ipadx=50, ipady=10)
        self.boton_info_detallada = tk.Button(self.resultado_analogia, text="Informacion Detallada de los Campos", command=self.ventana_informacion_detallada)
        self.boton_info_detallada.grid(row=1, column=1, ipadx=50, ipady=10)

    def resultado_analogia_jaccard(self):
        self.resultados,self.valores_nuevo_pozo,self.datos_pozos=self.calculo_analogia_jaccard()
        matrix_mostrar = []
        for i in range(len(self.datos_pozos[0]) + 1):
            fila = []
            for j in range(len(self.datos_pozos) + 1):
                if (j == 0 and i == 0):
                    fila.append('Puntaje(%)')
                elif (i == 0 and j == 1):
                    fila.append('Campo')
                elif (i == 0 and j not in [0, 1]):
                    fila.append(self.clase_base_de_datos.lista_propiedades_unidades(self.valores_nuevo_pozo[j - 1][i]))
                elif (i != 0 and j == 0):
                    if (i != 1):
                        fila.append(str(self.get_valor_resultado(self.resultados, self.datos_pozos[j][i - 1])))
                    else:
                        fila.append('100.0')
                elif (i != 0 and j == 1):
                    if (i == 1):
                        fila.append(self.valores_nuevo_pozo[0][i])
                    else:
                        fila.append(self.datos_pozos[0][i - 1])
                else:
                    if (i == 1):
                        fila.append(self.get_valor_to_string(self.valores_nuevo_pozo[j - 1][i]))
                    else:
                        fila.append(self.get_valor_to_string(self.datos_pozos[j - 1][i - 1]))
            matrix_mostrar.append(fila)
        self.analogia.destroy()
        self.resultado_analogia = tk.Toplevel()
        self.resultado_analogia.title("Resultado de la analogia del Campo: " + self.valores_nuevo_pozo[0][1])
        self.resultado_analogia.geometry("525x290+50+20")
        self.resultado_analogia.grid()
        self.resultado_analogia.rowconfigure(0, weight=9)
        self.resultado_analogia.rowconfigure(1, weight=1)
        self.resultado_analogia.columnconfigure(0, weight=1)
        self.resultado_analogia.columnconfigure(1, weight=1)
        self.frame_tabla_analogia = tk.Frame(self.resultado_analogia)
        matrix_mostrar = np.asarray(matrix_mostrar)
        self.df_matrix = pd.DataFrame(data=matrix_mostrar[1:, :], columns=matrix_mostrar[0, :])
        self.df_matrix = self.df_matrix.reindex(index=self.ordenar_dataframe())
        self.tabla_analogia = Table(self.frame_tabla_analogia, dataframe=self.df_matrix, showstatusbar=False,showtoolbar=False)
        self.tabla_analogia.show()
        self.frame_tabla_analogia.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.boton_exportar_excel_analogia = tk.Button(self.resultado_analogia, text="Exportar a Excel", command=self.ventana_guardar_excel_analogia)
        self.boton_exportar_excel_analogia.grid(row=1, column=0, ipadx=50, ipady=10)
        self.boton_info_detallada = tk.Button(self.resultado_analogia, text="Informacion Detallada de los Campos",command=self.ventana_informacion_detallada)
        self.boton_info_detallada.grid(row=1, column=1, ipadx=50, ipady=10)

    def calculo_analogia_promedio(self):
        filas_llenadas,valor_puntual,flag = self.comprobar_filas_llenadas()
        if flag:
            matrix_comparar=self.generacion_matrix_nuevo_pozo(filas_llenadas,valor_puntual)
            matrix_datos=self.clase_base_de_datos.get_matrix_valores_comparacion(filas_llenadas)
            matrix_diferencias=self.clase_base_de_datos.calculo_diferencias_propiedades(matrix_datos,matrix_comparar)
            matrix_resultado = []
            for i in range(1 + len(filas_llenadas)):
                fila = []
                for j in range(len(matrix_datos[0])):
                    if (j == 0 and i == 0):
                        fila.append('Campo')
                    elif (i == 0 and j != 0):
                        fila.append(self.clase_base_de_datos.get_pozos()[j-1])
                    elif (j == 0 and i != 0):
                        fila.append(self.clase_base_de_datos.lista_propiedades_analogia()[0][filas_llenadas[i - 1]])
                    else:
                        if (type(matrix_comparar[i][1]).__name__ == 'list' and type(
                                matrix_datos[i][j]).__name__ == 'list'):
                            AuB = []
                            for k in matrix_datos[i][j]:
                                AuB.append(k)
                            AnB = []
                            for x in matrix_comparar[i][1]:
                                if x not in AuB:
                                    AuB.append(x)
                                else:
                                    AnB.append(x)
                            fila.append(sum(AnB) / sum(AuB))
                        elif (type(matrix_comparar[i][1]).__name__ == 'list' or type(
                                matrix_datos[i][j]).__name__ == 'list'):
                            if (type(matrix_comparar[i][1]).__name__ == 'list'):
                                fila.append(1.0 if matrix_datos[i][j] in matrix_comparar[i][1] else 0)
                            else:
                                fila.append(1.0 if matrix_comparar[i][1] in matrix_datos[i][j] else 0)
                        elif (matrix_datos[i][j]==''):
                            fila.append(0)
                        else:
                            fila.append(1-(matrix_diferencias[i][j]*1.0 / max([matrix_diferencias[i][k] for k in range(1,len(matrix_diferencias[0]))])))
                matrix_resultado.append(fila)
            return matrix_resultado,matrix_comparar,matrix_datos
        else:
            return messagebox.showerror("Error en la analogia",
                                 "Digite correctamente los datos para realizar la \nla analogia del pozo digitado",parent=self.analogia),None,None

    def calculo_analogia_jaccard(self):
        filas_llenadas,valor_puntual, flag = self.comprobar_filas_llenadas()
        if flag:
            matrix_comparar = self.generacion_matrix_nuevo_pozo(filas_llenadas, valor_puntual)
            matrix_datos = self.clase_base_de_datos.get_matrix_valores_comparacion(filas_llenadas)
            matrix_diferencias = self.clase_base_de_datos.calculo_diferencias_propiedades(matrix_datos, matrix_comparar)
            matrix_resultado=[]
            for i in range(1+len(filas_llenadas)):
                fila=[]
                for j in range(len(matrix_datos[0])):
                    if (j == 0 and i == 0):
                        fila.append('Campo')
                    elif (i == 0 and j != 0):
                        fila.append(self.clase_base_de_datos.get_pozos()[j-1])
                    elif (j == 0 and i != 0):
                        fila.append(self.clase_base_de_datos.lista_propiedades_analogia()[0][filas_llenadas[i - 1]])
                    else:
                        if(type(matrix_comparar[i][1]).__name__=='list' and type(matrix_datos[i][j]).__name__=='list'):
                            AuB = []
                            for k in matrix_datos[i][j]:
                                AuB.append(k)
                            AnB = []
                            for x in matrix_comparar[i][1]:
                                if x not in AuB:
                                    AuB.append(x)
                                else:
                                    AnB.append(x)
                            fila.append(sum(AnB)/sum(AuB))
                        elif(type(matrix_comparar[i][1]).__name__=='list' or type(matrix_datos[i][j]).__name__=='list'):
                            if(type(matrix_comparar[i][1]).__name__=='list'):
                                fila.append(1.0 if matrix_datos[i][j] in matrix_comparar[i][1] else 0)
                            else:
                                fila.append(1.0 if matrix_comparar[i][1] in matrix_datos[i][j] else 0)
                        elif (matrix_datos[i][j]==''):
                            fila.append(0)
                        else:
                            fila.append(1.0-(matrix_diferencias[i][j]*1.0/max([matrix_diferencias[i][k] for k in range(1,len(matrix_diferencias[0]))])))
                matrix_resultado.append(fila)
            return matrix_resultado,matrix_comparar,matrix_datos
        else:
            return messagebox.showerror("Error en la analogia",
                                 "Digite correctamente los datos para realizar la \nla analogia del pozo digitado",parent=self.analogia),None,None

    def comprobar_filas_llenadas(self):
        filas_llenadas = [] #En este vector se guarda los indices de las filas que se han llenado en los entry's
        valor_puntual=[] #En este vector se guarda la informacion si corresponde a un valor puntual o un rango
        if (len(self.campo_nombre_pozo.get())!=0):
            contador_ponderado=0
            for i in range(0, len(self.matrix_valores[0])):
                if (len(self.matrix_valores[0][i].get()) != 0 and (
                        len(self.matrix_valores[1][i].get()) == 0 and len(self.matrix_valores[2][i].get()) == 0) and len(
                        self.matrix_valores[3][i].get()) != 0):
                    filas_llenadas.append(i)
                    valor_puntual.append(True)
                    contador_ponderado=contador_ponderado + float(self.matrix_valores[3][i].get())
                elif (len(self.matrix_valores[0][i].get()) == 0 and (
                        len(self.matrix_valores[1][i].get()) != 0 and len(self.matrix_valores[2][i].get()) != 0) and len(
                        self.matrix_valores[3][i].get()) != 0):
                    filas_llenadas.append(i)
                    valor_puntual.append(False)
                    contador_ponderado = contador_ponderado + float(self.matrix_valores[3][i].get())
                elif (len(self.matrix_valores[0][i].get()) == 0 and (
                        len(self.matrix_valores[1][i].get()) == 0 and len(self.matrix_valores[2][i].get()) == 0) and len(
                        self.matrix_valores[3][i].get()) == 0):
                    pass
                else:
                    filas_llenadas.append('error')
            if filas_llenadas == [] or 'error' in filas_llenadas or contador_ponderado not in [100.0,100.000000000000008,100.000000000000002]:
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
                    fila.append('Campo')
                elif (i == 0 and j != 0):
                    fila.append(self.campo_nombre_pozo.get())
                elif (j == 0 and i != 0):
                    fila.append(self.clase_base_de_datos.lista_propiedades_analogia()[0][filas_llenadas[i - 1]])
                else:
                    if (valor_puntual[i - 1]):
                        fila.append(float(self.matrix_valores[0][filas_llenadas[i-1]].get()))
                    else:
                        fila.append([float(k) for k in range(int(self.matrix_valores[1][filas_llenadas[i-1]].get()),int(self.matrix_valores[2][filas_llenadas[i-1]].get())+1)])
            matrix_comparar.append(fila)
        return matrix_comparar

    def get_valor_resultado(self,resultados,nomnbre_pozo):
        filas_llenadas=self.comprobar_filas_llenadas()[0]
        resultado=0
        for i in range(1,len(resultados[0])):
            if(resultados[0][i] == nomnbre_pozo):
                for j in range(1,len(resultados)):
                    resultado=resultado+resultados[j][i]*(float(self.matrix_valores[3][filas_llenadas[j-1]].get())/100)
        return resultado*100

    def get_valor_to_string(self,valor):
        if(type(valor).__name__ == 'list'):
            return str(valor[0])+' - '+str(valor[-1])
        else:
            return str(valor)

    def ventana_guardar_excel_consulta(self):
        filedirectory=filedialog.asksaveasfilename(title="Guardar como...",defaultextension='.xlsx',initialfile="Datos_consulta",parent=self.resultado)
        self.clase_base_de_datos.conversion_excel(self.busqueda_to_dataframe,filedirectory)

    def ventana_guardar_excel_analogia(self):
        filedirectory = filedialog.asksaveasfilename(title="Guardar como...", defaultextension='.xlsx',
                                                         initialfile="Resultado_analogia", parent=self.resultado_analogia)
        self.clase_base_de_datos.conversion_excel(self.df_matrix, filedirectory)

    def ventana_informacion_detallada(self):
        self.informacion_detallada=tk.Toplevel()
        self.informacion_detallada.title("Consulta de informacion detallada de los Campos Existentes")
        self.informacion_detallada.geometry("800x600+70+20")
        self.informacion_detallada.config(bg="#fff")
        self.informacion_detallada.grid()
        self.informacion_detallada.rowconfigure(0,weight=1)
        self.informacion_detallada.rowconfigure(1, weight =1)
        self.informacion_detallada.rowconfigure(2, weight =6)
        self.informacion_detallada.rowconfigure(3, weight =1)
        self.informacion_detallada.rowconfigure(4, weight =5)
        self.informacion_detallada.columnconfigure(0, weight =2)
        self.informacion_detallada.columnconfigure(1, weight =1)
        self.informacion_detallada.columnconfigure(2, weight=2)
        self.informacion_detallada.columnconfigure(3, weight=1)
        label_pozos=tk.Label(self.informacion_detallada,text="Seleccione un campo:",bg="#fff")
        self.lista_campos=ttk.Combobox(self.informacion_detallada,state="readonly",values=self.clase_base_de_datos.get_pozos())
        boton_mostrar=tk.Button(self.informacion_detallada,text="Mostrar datos del campo",command=self.mostrar_info_detallada)
        boton_mas_info=tk.Button(self.informacion_detallada,text="Mostrar mas informacion",command=self.ventana_mas_informacion)
        self.frame_tabla=tk.Frame(self.informacion_detallada)
        problemas_s=tk.Label(self.informacion_detallada,text="Problemas Estandar",bg="#76F072",relief="groove")
        self.texto_problemas_s=tk.Text(self.informacion_detallada,relief="groove",width=35,height=3)
        soluciones_s=tk.Label(self.informacion_detallada,text="Soluciones Estandar",bg="#76F072",relief="groove")
        self.texto_soluciones_s=tk.Text(self.informacion_detallada,relief="groove",width=35,height=3)
        myscroll3 = tk.Scrollbar(self.informacion_detallada, orient=tk.VERTICAL, command=self.texto_problemas_s.yview)
        myscroll4 = tk.Scrollbar(self.informacion_detallada, orient=tk.VERTICAL, command=self.texto_soluciones_s.yview)
        label_pozos.grid(row=0, column=0,columnspan=2, sticky=tk.N + tk.S + tk.E)
        self.lista_campos.grid(row=0, column=2,columnspan=2, sticky=tk.N + tk.S + tk.W)
        boton_mostrar.grid(row=1, column=0, columnspan=2, ipadx=30, ipady=6)
        boton_mas_info.grid(row=1, column=2, columnspan=2, ipadx=30, ipady=6)
        self.frame_tabla.grid(row=2,column=0,columnspan=4,sticky=tk.N + tk.S + tk.W + tk.E)
        problemas_s.grid(row=3, column=0,columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        soluciones_s.grid(row=3, column=2,columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        self.texto_problemas_s.grid(row=4, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        myscroll3.grid(row=4, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        self.texto_soluciones_s.grid(row=4,column=2, sticky=tk.N + tk.S + tk.W + tk.E)
        myscroll4.grid(row=4, column=3, sticky=tk.N + tk.S + tk.W + tk.E)

    def mostrar_info_detallada(self):
        if(len(self.lista_campos.get())==0):
            messagebox.showerror("Error en la consulta",
                                 "Digite los datos faltantes para realizar la \nla consulta en la base de datos",
                                 parent=self.informacion_detallada)
        else:
            matrix=self.clase_base_de_datos.get_problemas_soluciones_pozo(self.lista_campos.get())
            datos_ignicion=np.asarray(self.clase_base_de_datos.get_datos_ignicion_pozo(self.lista_campos.get()))
            datos_ignicion=pd.DataFrame(data=datos_ignicion[1:,:],columns=datos_ignicion[0,:])
            tabla=Table(self.frame_tabla,dataframe=datos_ignicion,showtoolbar=False,showstatusbar=False)
            tabla.show()
            problemas_s=self.ordenar_texto_indices(matrix[3][1])
            soluciones_s=self.ordenar_texto_indices(matrix[4][1])
            self.informacion_detallada.update_idletasks() # Con esto actualizo la informacion de la ventana como el tamaño y demas
            caracteres=round(0.0854166*self.informacion_detallada.winfo_width())
            lineas=round(0.0171296*self.informacion_detallada.winfo_height())
            self.texto_problemas_s.delete(1.0,tk.END)
            self.texto_soluciones_s.delete(1.0,tk.END)
            self.texto_problemas_s.config(width=caracteres, height=lineas)
            self.texto_soluciones_s.config(width=caracteres, height=lineas)
            self.texto_problemas_s.insert(tk.END,problemas_s)
            self.texto_soluciones_s.insert(tk.END,soluciones_s)

    def ordenar_texto_indices(self,texto): #Funcion que se encarga de ordenar bonito los numerales como 1) o A.
        indicador=[41,46]
        letras=list(range(65,91))
        numeros=list(range(48,58))
        memoria=0
        i=2
        while(i<len(texto)):
            if(memoria):
                if(ord(texto[i]) in indicador):
                    mit1=texto[0:i-1]
                    mit2=texto[i-1:len(texto)+1]
                    texto=mit1+"\n"+mit2
                    memoria=0
                else:
                    memoria=0
            else:
                if(ord(texto[i]) in letras or ord(texto[i]) in numeros):
                    memoria=1
            i = i + 1
        return texto

    def ventana_mas_informacion(self):
        if (len(self.lista_campos.get()) == 0):
            messagebox.showerror("Error en la consulta",
                                 "Digite los datos faltantes para realizar la \nla consulta en la base de datos",
                                 parent=self.informacion_detallada)
        else:
            matrix = self.clase_base_de_datos.get_problemas_soluciones_pozo(self.lista_campos.get())
            mas_info=tk.Toplevel()
            mas_info.title("Mas informacion sobre el pozo " + self.lista_campos.get())
            mas_info.geometry("850x325+140+30")
            mas_info.grid()
            mas_info.rowconfigure(0, weight=1)
            mas_info.rowconfigure(1, weight=5)
            mas_info.rowconfigure(2, weight=1)
            mas_info.rowconfigure(3, weight=5)
            mas_info.columnconfigure(0, weight=2)
            mas_info.columnconfigure(1, weight=1)
            mas_info.columnconfigure(2, weight=2)
            mas_info.columnconfigure(3, weight=1)
            mas_info.update_idletasks()  # Con esto actualizo la informacion de la ventana como el tamaño y demas
            caracteres = round(0.0854166 * mas_info.winfo_width())
            lineas = round(0.0171296 * mas_info.winfo_height())
            problemas = tk.Label(mas_info, text="Problemas", bg="#76F072", relief="groove")
            texto_problemas = tk.Text(mas_info, relief="groove", width=caracteres, height=lineas)
            soluciones = tk.Label(mas_info, text="Soluciones", bg="#76F072", relief="groove")
            texto_soluciones = tk.Text(mas_info, relief="groove", width=caracteres, height=lineas)
            metodos1 = tk.Label(mas_info, text="Metodos para detectar la etapa en laboratorio", bg="#76F072", relief="groove")
            texto_metodos1 = tk.Text(mas_info, relief="groove", width=caracteres, height=lineas)
            metodos2 = tk.Label(mas_info, text="Metodos para detectar la etapa en campo", bg="#76F072", relief="groove")
            texto_metodos2 = tk.Text(mas_info, relief="groove", width=caracteres, height=lineas)
            myscroll1 = tk.Scrollbar(mas_info, orient=tk.VERTICAL, command=texto_problemas.yview)
            myscroll2 = tk.Scrollbar(mas_info, orient=tk.VERTICAL,
                                     command=texto_soluciones.yview)
            myscroll3 = tk.Scrollbar(mas_info, orient=tk.VERTICAL,
                                     command=texto_metodos1.yview)
            myscroll4 = tk.Scrollbar(mas_info, orient=tk.VERTICAL,
                                     command=texto_metodos2.yview)
            problemas.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
            soluciones.grid(row=0, column=2, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
            texto_problemas.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
            myscroll1.grid(row=1, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
            texto_soluciones.grid(row=1, column=2, sticky=tk.N + tk.S + tk.W + tk.E)
            myscroll2.grid(row=1, column=3, sticky=tk.N + tk.S + tk.W + tk.E)
            metodos1.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
            metodos2.grid(row=2, column=2, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
            texto_metodos1.grid(row=3, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
            myscroll3.grid(row=3, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
            texto_metodos2.grid(row=3, column=2, sticky=tk.N + tk.S + tk.W + tk.E)
            myscroll4.grid(row=3, column=3, sticky=tk.N + tk.S + tk.W + tk.E)
            texto_problemas.insert(tk.END, self.ordenar_texto_indices(matrix[1][1]))
            texto_soluciones.insert(tk.END, self.ordenar_texto_indices(matrix[2][1]))
            texto_metodos1.insert(tk.END, self.ordenar_texto_indices(matrix[5][1]))
            texto_metodos2.insert(tk.END, self.ordenar_texto_indices(matrix[6][1]))

    def ordenar_dataframe(self):
        filas=list(self.df_matrix["Puntaje(%)"].values)
        for i in range(len(filas)):
            filas[i]=[float(filas[i]),i]
        filas=sorted(filas,reverse=True)
        indices=[]
        for i in range(len(filas)):
            indices.append(filas[i][1])
        return indices

app=Application()
app.master.title("SOFTWARE D.I.S")
app.master.resizable(0,0)
app.master.geometry("800x600+50+20")
app.mainloop()

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
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
        self.boton_consulta = tk.Button(self, text='Consultar Campo',command=self.ventana_consulta)
        self.boton_consulta.grid(row=1,column=0,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)
        self.boton_analogia = tk.Button(self, text='Realizar Analogia',command=self.ventana_analogia)
        self.boton_analogia.grid(row=1,column=1,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)

    def ventana_consulta(self):
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

    def resultado_consulta(self):
        if(len(self.lista_pozos.get()) == 0):# or len(self.lista_categorias.get()) == 0):
            messagebox.showerror("Error en la consulta","Digite los datos faltantes para realizar la \nla consulta en la base de datos",parent=self.consulta)
        else:
            pozo=self.lista_pozos.get()
            self.consulta.destroy()
            self.resultado = tk.Toplevel()
            self.resultado.title("Resultado de la consulta del campo: "+ pozo)
            self.resultado.geometry("800x600+50+20")
            self.resultado.grid()
            self.resultado.rowconfigure(0,weight=9)
            self.resultado.rowconfigure(1,weight=1)
            self.resultado.columnconfigure(0,weight=1)
            self.frame_tabla_consulta=tk.Frame(self.resultado)
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
            self.busqueda_to_dataframe = pd.DataFrame(data=busqueda[1:,:],columns=busqueda[0,:])
            self.table = Table(self.frame_tabla_consulta,dataframe=self.busqueda_to_dataframe,showstatusbar=False,showtoolbar=False) #Con este table puedo mostrar la tabla de consulta
            self.table.show()
            self.frame_tabla_consulta.grid(row=0,column=0,sticky=tk.N+tk.S+tk.W+tk.E)
            self.boton_exportar_excel_consulta=tk.Button(self.resultado,text="Exportar a Excel",command=self.ventana_guardar_excel_consulta)
            self.boton_exportar_excel_consulta.grid(row=1,column=0,ipadx=50,ipady=10)

    def ventana_analogia(self):
        self.analogia = tk.Toplevel()
        self.analogia.title("Modulo para realizar analogia de un nuevo campo")
        self.analogia.geometry("850x325+70+30")
        self.analogia.config(bg="#fff")
        self.analogia.grid()
        for i in range(0, 11):
            self.analogia.rowconfigure(i, weight=1)
        for i in range(0, 6):
            self.analogia.columnconfigure(i, weight=1)
        self.nombre_pozo = tk.Label(self.analogia, text="Nombre del campo:", bg="#E8F06B", relief="groove")
        self.campo_nombre_pozo  = tk.Entry(self.analogia,bg="#E2EBC8",relief="groove",justify=tk.CENTER)
        self.propiedades = tk.Label(self.analogia, text="Propiedades para analogia", bg="#E8F06B", relief="groove")
        self.unidades = tk.Label(self.analogia, text="Unidades", bg="#E8F06B", relief="groove")
        self.puntual = tk.Label(self.analogia, text="Valor único", bg="#E8F06B", relief="groove")
        self.min = tk.Label(self.analogia, text="Valor minimo", bg="#E8F06B", relief="groove")
        self.max = tk.Label(self.analogia, text="Valor maximo", bg="#E8F06B", relief="groove")
        self.ponderacion = tk.Label(self.analogia, text="Ponderacion(%)", bg="#E8F06B", relief="groove")
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
            propiedad = tk.Label(self.analogia,text=propi_unida[0][i],bg="#76F072",relief="groove")
            unidades = tk.Label(self.analogia,text=propi_unida[1][i],bg="#76F072",relief="groove")
            propiedad.grid(row=2+i,column=0,sticky=tk.N + tk.S + tk.W + tk.E)
            unidades.grid(row=2+i,column=1,sticky=tk.N + tk.S + tk.W + tk.E)
        self.matrix_valores=[]
        for j in range(0,4):
            columna=[]
            for i in range(0,8):
                valor_ingresar = tk.Entry(self.analogia,bg="#E2EBC8",justify=tk.CENTER,relief="groove")
                valor_ingresar.grid(row=2+i, column=2+j, sticky=tk.N + tk.S + tk.W + tk.E)
                columna.append(valor_ingresar)
            self.matrix_valores.append(columna)
        self.boton_ponderado = tk.Button(self.analogia,text="Establecer Ponderaciones",command=self.set_ponderaciones)
        self.boton_analogia_promedio = tk.Button(self.analogia,text="Realizar Analogia por Valor Promedio",command=self.resultado_analogia_promedio)
        self.boton_analogia_jaccard = tk.Button(self.analogia,text="Realizar Analogia por Jaccard",command=self.resultado_analogia_jaccard)
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
                        fila.append('')
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
                        fila.append('')
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
                            fila.append(matrix_diferencias[i][j]*1.0 / max([matrix_diferencias[i][k] for k in range(1,len(matrix_diferencias[0]))]))
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
                        elif (type(matrix_datos[i][j]=='')):
                            fila.append(0)
                        else:
                            fila.append(1-(matrix_diferencias[i][j]/max([matrix_diferencias[i][k] for k in range(1,len(matrix_diferencias[0]))])))
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
        self.informacion_detallada.rowconfigure(2, weight =1)
        self.informacion_detallada.rowconfigure(3, weight =5)
        self.informacion_detallada.rowconfigure(4, weight =1)
        self.informacion_detallada.rowconfigure(5, weight =5)
        self.informacion_detallada.columnconfigure(0, weight =1)
        self.informacion_detallada.columnconfigure(1, weight =1)
        label_pozos=tk.Label(self.informacion_detallada,text="Seleccione un campo:",bg="#fff")
        self.lista_campos=ttk.Combobox(self.informacion_detallada,state="readonly",values=self.clase_base_de_datos.get_pozos())
        boton_mostrar=tk.Button(self.informacion_detallada,text="Mostrar datos del campo",command=self.mostrar_info_detallada)
        problemas=tk.Label(self.informacion_detallada,text="Problemas",bg="#76F072",relief="groove")
        self.texto_problemas=tk.Label(self.informacion_detallada,bg="#fff",relief="groove",justify=tk.LEFT)
        soluciones=tk.Label(self.informacion_detallada,text="Soluciones",bg="#76F072",relief="groove")
        self.texto_soluciones=tk.Label(self.informacion_detallada,bg="#fff",relief="groove",justify=tk.LEFT)
        problemas_s=tk.Label(self.informacion_detallada,text="Problemas Estandar",bg="#76F072",relief="groove")
        self.texto_problemas_s=tk.Label(self.informacion_detallada,bg="#fff",relief="groove",justify=tk.LEFT)
        soluciones_s=tk.Label(self.informacion_detallada,text="Soluciones Estandar",bg="#76F072",relief="groove")
        self.texto_solciones_s=tk.Label(self.informacion_detallada,bg="#fff",relief="groove",justify=tk.LEFT)
        label_pozos.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E)
        self.lista_campos.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W)
        boton_mostrar.grid(row=1, column=0, columnspan=2, ipadx=30, ipady=6)
        problemas.grid(row=2, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        soluciones.grid(row=2, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        self.texto_problemas.grid(row=3, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.texto_soluciones.grid(row=3, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        problemas_s.grid(row=4, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        soluciones_s.grid(row=4, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        self.texto_problemas_s.grid(row=5, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.texto_solciones_s.grid(row=5,column=1, sticky=tk.N + tk.S + tk.W + tk.E)

    def mostrar_info_detallada(self):
        if(len(self.lista_campos.get())==0):
            messagebox.showerror("Error en la consulta",
                                 "Digite los datos faltantes para realizar la \nla consulta en la base de datos",
                                 parent=self.informacion_detallada)
        else:
            matrix=self.clase_base_de_datos.get_problemas_soluciones_pozo(self.lista_campos.get())
            problemas=self.ordenar_texto_indices(matrix[1][1])
            soluciones=self.ordenar_texto_indices(matrix[2][1])
            problemas_s=self.ordenar_texto_indices(matrix[3][1])
            soluciones_s=self.ordenar_texto_indices(matrix[4][1])
            #self.informacion_detallada.update_idletasks() # Con esto actualizo la informacion de la ventana como el tamaño y demas
            n=round(0.1*self.informacion_detallada.winfo_width())
            n=60
            """self.texto_problemas.config(text=self.seccionado_texto(problemas,n),justify=tk.LEFT)
            self.texto_soluciones.config(text=self.seccionado_texto(soluciones,n),justify=tk.LEFT)
            self.texto_problemas_s.config(text=self.seccionado_texto(problemas_s,n),justify=tk.LEFT)
            self.texto_solciones_s.config(text=self.seccionado_texto(soluciones_s,n),justify=tk.LEFT)"""
            self.texto_problemas.config(text=problemas, justify=tk.LEFT)
            self.texto_soluciones.config(text=soluciones, justify=tk.LEFT)
            self.texto_problemas_s.config(text=problemas_s, justify=tk.LEFT)
            self.texto_solciones_s.config(text=soluciones_s, justify=tk.LEFT)

    def seccionado_texto(self,texto,n): #Funcion que secciona el texto para que salga  completo
        """i=0
        while(i+n<len(texto)+1):
            if(texto.find('\n',beg=i)-i > n):
                mit1=texto[0:i+n+1]s
                mit2=texto[i+n+1:len(texto)+1]
                texto=mit1+"\n"+mit2
                i=i+n
            else:
                i=texto.find('\n',beg=i)+2
        return texto"""


    def ordenar_texto_indices(self,texto): #Funcion que se encarga de ordenar bonito los numerales como 1) o A.
        indicador=[41,46]
        letras=list(range(65,91))
        numeros=list(range(48,58))
        memoria=0
        for i in range(2,len(texto)):
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
        return texto

app=Application()
app.master.title("SOFTWARE D.I.S")
app.master.resizable(0,0)
app.master.geometry("800x600+50+20")
app.mainloop()

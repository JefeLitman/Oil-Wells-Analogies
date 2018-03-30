import numpy as np
import pandas as pd

class base_datos():

    def __init__(self):
        self.datos=pd.DataFrame()

    def cargar_datos(self): #Funcion que retorna los datos de la base de datos ordenados y listos para trabajar
        self.datos=pd.read_csv("base_datos.csv",header=None) #Con este comando podemos leer la base de datos del excel que fue exportado a csv
        # #Funcion para renombrar las columnas y filas de la base de datos para que quede mas bonita
        for i in range(2,self.datos.shape[0],1):
            if (str(self.datos.at[i, 0]) == 'nan'):
                self.datos.at[i, 0] = self.datos.at[i - 1, 0]

        for i in range(0,self.datos.shape[1],1):
            if(str(self.datos.at[0,i]) == 'nan'):
                if(i-1 > 0):
                    self.datos.at[0,i] =self.datos.at[0,i-1]
                elif(i > 0):
                    self.datos.at[0,i] ="Propiedades"
                else:
                    self.datos.at[0,i] ="Categorias"

        for j in self.datos.columns: #Funcion para cambiar los nan por " " que serian los espacios en blanco
            for i in range(0,np.shape(self.datos)[0],1):
                if (str(self.datos.at[i,j])=='nan'):
                    self.datos.at[i,j]=""
        return self.datos # Retorno de los datos ordenados y arreglados

    def conversion_excel(self):
        self.datos.to_excel(pd.ExcelWriter('base_datos1.xlsx'),'Sheet1') #Como convertir de dataframe a excel

    def get_pozos(self): # Funcion que retorna una lista de los pozos listados en la base de datos
        pozos=[]
        for i in range(2,self.datos.shape[1],1):
            pozos.append(self.datos.at[0,i])
        pozos=list(set(pozos))
        return pozos

    def get_categorias(self): #Funcion que retorna una lista de las categorias listadas en la base de datos
        categorias=[]
        for i in range(2,self.datos.shape[0],1):
            categorias.append(self.datos.at[i, 0])
        categorias=list(set(categorias))
        return categorias

    def get_valores_pozo(self,pozo): #Funcion que retorna una matriz todos los valores del pozo mandado
        categorias = self.get_categorias()
        cols=[0,1]
        for i in range(0,self.datos.shape[1],1):
            if (self.datos.at[0, i] == pozo):
                cols.append(i)
        cats=[1]
        for categoria in categorias:
            for i in range(0,self.datos.shape[0],1):
                if (self.datos.at[i, 0] == categoria):
                    cats.append(i)
        busqueda = []
        for i in cats:
            fila = []
            for j in cols:
                fila.append(self.datos.at[i, j])
            busqueda.append(fila)
        return busqueda

    def lista_propiedades_analogia(self): #Funcion que retorna las propiedades y unidades para realizar la analogia
        propiedades = [
            "Viscosidad del crudo",
            "Espesor neto",
            "Gravedad API del crudo",
            "Permeabilidad",
            "Porosidad",
            "Presion del yacimiento al inicio del proyecto",
            "Temperatura del yacimiento",
            "Profundidad"
        ]
        unidades=[
            'cp',
            'ft',
            '°API',
            'md',
            '%',
            'psi',
            "°F",
            "ft"
        ]
        propi_unida = [propiedades,unidades]
        return propi_unida

    def get_matrix_valores_comparacion(self,filas_llenadas,valor_puntual): #Funcion que retorna los valores en la base
        #de datos para tener los valores teoricos a realizar la comparacion
        propiedades=self.lista_propiedades_analogia()[0]
        matrix_valores=[]
        for i in range(1+len(filas_llenadas)):
            fila = []
            for j in range(1 + len(self.get_pozos())):
                if (j == 0 and i == 0):
                    fila.append('Pozo')
                elif (i == 0 and j != 0):
                    fila.append(self.get_pozos()[j - 1])
                elif (j == 0 and i != 0):
                    fila.append(propiedades[filas_llenadas[i - 1]])
                else:
                    pass #Aqui debera ir agregando los valores para la propiedad i del pozo j
            matrix_valores.append(fila)
        return matrix_valores

    def get_valor_propiedad_del_pozo(self,propiedad,pozo):
        indices
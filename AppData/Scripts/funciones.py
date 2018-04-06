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

    def conversion_excel(self,datos_a_convertir,filedirectory):
        if (filedirectory != ''):
            datos_a_convertir.to_excel(pd.ExcelWriter(filedirectory),'Sheet1') #Como convertir de dataframe a excel

    def get_pozos(self): # Funcion que retorna una lista de los pozos listados en la base de datos
        pozos=[]
        for i in range(2,self.datos.shape[1],1):
            pozos.append(self.datos.at[0,i])
        d={}
        pozos=[d.setdefault(x, x) for x in pozos if x not in d]
        return pozos

    def get_categorias(self): #Funcion que retorna una lista de las categorias listadas en la base de datos
        categorias=[]
        for i in range(2,self.datos.shape[0],1):
            categorias.append(self.datos.at[i, 0])
        d = {}
        categorias=[d.setdefault(x, x) for x in categorias if x not in d]
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

    def get_matrix_valores_comparacion(self,filas_llenadas): #Funcion que retorna los valores en la base
        #de datos para tener los valores teoricos a realizar la comparacion
        propiedades=self.lista_propiedades_analogia()[0]
        matrix_valores=[]
        for i in range(1+len(filas_llenadas)):
            fila = []
            for j in range(1 + len(self.get_pozos())):
                if (j == 0 and i == 0):
                    fila.append('Campo')
                elif (i == 0 and j != 0):
                    fila.append(self.get_pozos()[j - 1])
                elif (j == 0 and i != 0):
                    fila.append(propiedades[filas_llenadas[i - 1]])
                else:
                    fila.append(self.get_valor_propiedad_del_pozo(fila[0],matrix_valores[0][j]))
            matrix_valores.append(fila)
        return matrix_valores

    def get_valor_propiedad_del_pozo(self,propiedad,pozo): #Funcion que retorna el valor del pozo para determinada propiedad
        for i in range(self.datos.shape[0]):
            if(self.datos.at[i,1]==propiedad):
                indice_fila=i
        for j in range(3,self.datos.shape[1]-1,3):
            if (self.datos.at[0, j] == pozo):
                indice_columna=j
        if '-' in self.datos.at[indice_fila,indice_columna]:
            valor_min=''
            valor_max=''
            flag=False
            for x in self.datos.at[indice_fila,indice_columna]:
                if ((x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '0') and flag==0):
                    valor_min=valor_min+x
                elif(x == '-' and flag==0):
                    flag=True
                elif((x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '0') and flag):
                    valor_max=valor_max+x
            if (valor_min=='' or valor_max==''):
                return self.datos.at[indice_fila,indice_columna]
            else:
                return [int(i) for i in range(int(valor_min),int(valor_max)+1,1)]
        elif(self.datos.at[indice_fila,indice_columna]==''):
            return ''
        else:
            return float(self.datos.at[indice_fila,indice_columna])

    def calculo_diferencias_propiedades(self,matrix_datos,matrix_comparar):
        matrix_diferencias=[]
        for i in range(len(matrix_datos)):
            fila=[]
            for j in range(len(matrix_datos[0])):
                if (j == 0 and i == 0):
                    fila.append('Campo')
                elif (i == 0 and j != 0):
                    fila.append(self.get_pozos()[j - 1])
                elif (j == 0 and i != 0):
                    fila.append(matrix_datos[i][j])
                else:
                    if(type(matrix_datos[i][j]).__name__ == 'list'):
                        valor_datos=(matrix_datos[i][j][0]+matrix_datos[i][j][-1])/2
                    elif(type(matrix_datos[i][j]).__name__=='str'):
                        valor_datos=0
                    else:
                        valor_datos=matrix_datos[i][j]
                    if(type(matrix_comparar[i][1]).__name__ == 'list'):
                        valor_comparar=(matrix_comparar[i][1][0]+matrix_comparar[i][1][-1])/2
                    else:
                        valor_comparar=matrix_comparar[i][1]
                    if(valor_datos==0):
                        fila.append(0.0)
                    else:
                        fila.append(1.0*abs(valor_datos - valor_comparar))
            matrix_diferencias.append(fila)
        return matrix_diferencias

    def lista_propiedades_unidades(self,propiedad): #Funcion que retorna las propiedades y unidades unidas
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
        for i in range(len(propiedades)):
            if (propiedades[i]==propiedad):
                return propiedades[i]+'('+unidades[i]+')'

    def get_problemas_soluciones_pozo(self,pozo):
        pass
import numpy as np
import pandas as pd

class base_datos():

    def __init__(self):
        self.datos=pd.DataFrame()

    def cargar_datos(self):
        self.datos=pd.read_csv("datos_prueba.csv") #Con este comando podemos leer la base de datos del excel que fue exportado a csv
        columns=[] #Funcion para renombrar al final las columnas y dejarlas bonitas antes de exportar a excel
        for i in range(0,len(self.datos.columns),1):
            if(self.datos.columns[i] == 'Unnamed: '+str(i)):
                if(i-1 > 0):
                    columns.append(columns[i-1][:-1*len(str(i))]+str(i))
                elif(i > 0):
                    columns.append("Propiedades1")
                else:
                    columns.append("Categorias0")
            else:
                    columns.append(self.datos.columns[i]+str(i))
        self.datos.columns=columns
        for j in self.datos.columns: #Funcion para cambiar los nan por 0's que serian los espacios en blanco
            for i in range(0,np.shape(self.datos)[0],1):
                if (str(self.datos.at[i,j])=='nan'):
                    self.datos.at[i,j]=" "
        return self.datos

    def conversion_excel(self):
        self.datos.to_excel(pd.ExcelWriter('base_de_datos.xlsx'),'Sheet1') #Como convertir de dataframe a excel

import tkinter as tk
import tkinter.font as tkFont
from AppData.Scripts.funciones import base_datos as bd
import numpy as np

base = bd()
datos=base.cargar_datos()
filas=[0,7]
matrix=base.get_matrix_valores_comparacion(filas,None)
print(matrix)

#pantalla = tk.Tk()
#for x in tkFont.families():
#    print(x)
#pantalla.mainloop()
import tkinter as tk
import tkinter.font as tkFont
from AppData.Scripts.funciones import base_datos as bd
import numpy as np

base = bd()
datos=base.cargar_datos()
for i in base.get_matrix_valores_comparacion([0,7]):
    print(i)

#pantalla = tk.Tk()
#for x in tkFont.families():
#    print(x)
#pantalla.mainloop()
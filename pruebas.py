import tkinter as tk
from tkinter import filedialog
#import tkinter.font as tkFont
#from AppData.Scripts.funciones import base_datos as bd
#import numpy as np

root = tk.Tk()
root.grid()
texto="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
for i in range(20,len(texto)+1):
    if(i%20==0):
        mitad=texto[0:i]
        otra_mitad=texto[i:len(texto)+1]
        nuevo_texto=mitad+"\n"+otra_mitad
text=tk.Label(root,text=texto,justify=tk.LEFT)
text.grid(sticky=tk.N+tk.S+tk.W+tk.E)
root.mainloop()

#base = bd()
#datos=base.cargar_datos()
#print(base.get_matrix_valores_comparacion([0,7])[2][3][])

#pantalla = tk.Tk()
#for x in tkFont.families():
#    print(x)
#pantalla.mainloop()
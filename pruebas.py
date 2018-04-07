import tkinter as tk
from tkinter import filedialog
#import tkinter.font as tkFont
from AppData.Scripts.funciones import base_datos as bd
#import numpy as np

#root = tk.Tk()
#root.geometry("400x400")
#root.grid()
#texto="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#n_caracteres=60
#for i in range(1,round(len(texto)/n_caracteres)):
#    mit1=texto[0:i*(n_caracteres+1)-1]
#    mit2=texto[i*(n_caracteres+1)-1:len(texto)+1]
#    texto=mit1+"\n"+mit2
#text=tk.Label(root,text=texto,justify=tk.LEFT)
#text.grid(sticky=tk.N+tk.S+tk.W+tk.E)
#root.mainloop()



pantalla = tk.Tk()
#for x in tkFont.families():
#    print(x)
pantalla.geometry("800x600")
pantalla.update_idletasks()
print(round(pantalla.winfo_width()*0.1))
pantalla.mainloop()
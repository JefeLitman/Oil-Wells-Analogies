import tkinter as tk
from tkinter import ttk
from math import ceil
from tkinter import filedialog
import tkinter.font as tkFont
from AppData.Scripts.funciones import base_datos as bd
import numpy as np

"""root = tk.Tk()
root.geometry("400x400")
root.grid()
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
texto="1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
n_caracteres=20
for i in range(1,ceil(len(texto)/n_caracteres)):
    mit1=texto[0:i*(n_caracteres+1)-1]
    mit2=texto[i*(n_caracteres+1)-1:len(texto)+1]
    texto=mit1+"\n"+mit2
#text=tk.Label(root,text=texto,justify=tk.LEFT)
#text1=tk.Label(root,text=texto,justify=tk.LEFT)
text=ttk.Entry(root,textvariable=tk.StringVar(value=texto),state='readonly')
myscroll = ttk.Scrollbar(root,orient='vertical',command=text.xview)
text.config(xscrollcommand=myscroll.set)
text.grid(row=0,column=0,sticky=tk.N+tk.W)
myscroll.grid(row=1,column=0,sticky=tk.E+tk.W)
root.mainloop()"""

root = tk.Tk()
root.geometry("200x200")
texto = '1234567890'*8
n_caracteres=20
for i in range(1,int(ceil(len(texto)/n_caracteres))):
    mit1=texto[0:i*(n_caracteres+1)-1]
    mit2=texto[i*(n_caracteres+1)-1:len(texto)+1]
    texto=mit1+"\n"+mit2
mytext = tk.Text(root,width=10,height=2)
mytext.insert(tk.END,texto)
myscroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=mytext.yview)
mytext.config(yscrollcommand=myscroll.set,state=tk.DISABLED)
mytext.grid(row=0,column=0, sticky=tk.N+tk.S+tk.W+tk.E)
myscroll.grid(row=0,column=1, sticky=tk.N+tk.S+tk.W+tk.E)

root.mainloop()

"""from tkinter import *

master = Tk()

w = Message(master, text="123456789012345678901234567890123456789012345678901234567890")
w.pack()

mainloop()"""
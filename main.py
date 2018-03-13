#from funciones import base_datos as bd
import tkinter as tk

class software_DIS(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.menu_principal()
        #self.grid_remove()


    def menu_principal(self):
        self.widgets_menu_principal()

    def widgets_menu_principal(self):
        self.imagen_fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")
        self.fondo=tk.Label(self,image=self.imagen_fondo).grid()
        self.boton_consulta = tk.Button(self, text="Consultar Pozo", bg="white", command=None)
        self.boton_analogia = tk.Button(self, text="Realizar Analogia", bg="white",command=None)
        self.boton_salir = tk.Button(self, text="Salir", bg="white", command=self.quit)

#menu_principal = tk.Tk()
#menu_principal.geometry("800x600+50+20")
#menu_principal.resizable(0,0)
#menu_principal.title("SOFTWARE D.I.S")
#fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")
#background=tk.Label(menu_principal,image=fondo).place(x=0,y=0,relwidth=1,relheight=1)
#boton_consulta=tk.Button(menu_principal,text="Consultar Pozo",bg="white",command=None).place(x=100,y=500)
#boton_analogia=tk.Button(menu_principal,text="Realizar Analogia",bg="white",command=prueba_borrado(boton_consulta)).place(x=350,y=500)
#boton_salir=tk.Button(menu_principal,text="Salir",bg="white",command=menu_principal.quit).place(x=600,y=500)

#menu_principal.mainloop()

app = software_DIS()
app.master.title("SOFTWARE D.I.S")
app.master.geometry("800x600+50+20")
app.master.resizable(0,0)
app.mainloop()
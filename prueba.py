import tkinter as tk

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.rowconfigure(1, weight =1)
        top.columnconfigure(0, weight =1)
        top.columnconfigure(1, weight =1)
        self.createWidgets()

    def createWidgets(self):
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight =1)
        self.columnconfigure(0, weight =1)
        self.columnconfigure(1, weight=1)
        self.imagen_fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")
        self.fondo_pantalla=tk.Label(self,image=self.imagen_fondo)
        self.fondo_pantalla.grid(row=0,column=0,rowspan=2,columnspan=2,sticky=tk.S+tk.N+tk.W+tk.E)
        self.boton_consulta = tk.Button(self, text='Consultar Pozo', command=self.ventana_consulta)
        self.boton_consulta.grid(row=1,column=0,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)
        self.boton_analogia = tk.Button(self, text='Realizar Analogia', command=self.ventana_analogia)
        self.boton_analogia.grid(row=1,column=1,padx=80,pady=100,sticky=tk.W+tk.E+tk.S)

    def ventana_consulta(self):
        consulta=tk.Toplevel()
        consulta.title("Consulta de Pozos existentes")



    def ventana_analogia(self):
        pass

app=Application()
app.master.title('Aplicacion de prueba')
app.master.resizable(0,0)
app.master.geometry("800x600+50+20")
app.mainloop()
import tkinter as tk

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()#sticky=tk.N+tk.S+tk.W+tk.E)
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        top.config(bg="black")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.consultaBoton = tk.Button(self, text='Consultar', command=None)
        self.analogiaBoton = tk.Button(self, text='Analogia', command=None)
        self.salirBoton = tk.Button(self,text='Salir',command=self.quit)
        self.consultaBoton.grid(row=1,column=0,sticky=tk.N+tk.S+tk.W+tk.E)
        self.analogiaBoton.grid(row=1,column=1,sticky=tk.N+tk.S+tk.W+tk.E)
        self.salirBoton.grid(row=1,column=2,sticky=tk.N+tk.S+tk.W+tk.E)

app=Application()
app.master.title('Aplicacion de prueba')
app.master.geometry("629x269")
#app.master.config(bg="black")
app.mainloop()
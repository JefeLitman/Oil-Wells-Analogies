import tkinter as tk

class software_DIS():
    def __init__(self):
        self.ventana_principal()

    def ventana_principal(self):
        self.menu_principal = tk.Tk()
        self.menu_principal.geometry("800x600+50+20")
        self.menu_principal.resizable(0,0)
        self.menu_principal.title("SOFTWARE D.I.S")
        self.fondo=tk.PhotoImage(file="AppData/Images/ecopetrol_bg.gif")

app = software_DIS()
app.ventana_principal()
app.menu_principal.mainloop()
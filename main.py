import tkinter as tk
from database.db import crear_base_de_datos
from gui.interfaz_principal import Aplicacion

if __name__ == "__main__":
    crear_base_de_datos()
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

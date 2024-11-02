import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.crud import registrar_vendedor

class InterfazRegistroVendedor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, pady=(10, 5))
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, pady=(10, 5))

        ttk.Label(self, text="Apellido:").grid(row=1, column=0, pady=(5, 5))
        self.entry_apellido = ttk.Entry(self)
        self.entry_apellido.grid(row=1, column=1, pady=(5, 5))

        # Botón de registro con estilo
        self.boton_registrar = ttk.Button(self, text="Registrar Vendedor", command=self.registrar)
        self.boton_registrar.grid(row=2, columnspan=2, pady=(20, 10))

        # Cambiar el color del botón (usando estilo)
        estilo = ttk.Style()
        estilo.configure("TButton", background="lightblue", foreground="black", padding=10, font=("Arial", 10, "bold"))
        self.boton_registrar.config(style="TButton")

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()

        # Validar que todos los campos estén llenos
        if not nombre or not apellido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Registrar el vendedor
        if registrar_vendedor(nombre, apellido):
            messagebox.showinfo("Éxito", "Vendedor registrado con éxito.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el vendedor.")

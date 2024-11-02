import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.crud import registrar_cliente

class InterfazRegistroCliente(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_apellido = ttk.Entry(self)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Dirección:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_direccion = ttk.Entry(self)
        self.entry_direccion.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_telefono = ttk.Entry(self, validate='key')  # Validación para el teléfono
        self.entry_telefono.grid(row=3, column=1, padx=5, pady=5)

        # Crear un validador que solo permite números para el teléfono
        vcmd_numero = (parent.register(self.validar_numero), '%P')
        self.entry_telefono.config(validate='key', validatecommand=vcmd_numero)

        # Botón de registro con estilo y separación
        self.boton_registrar = ttk.Button(self, text="Registrar Cliente", command=self.registrar)
        self.boton_registrar.grid(row=4, columnspan=2, pady=(20, 10))  # Añadido espacio arriba y abajo

        # Cambiar el color del botón (usando estilo)
        estilo = ttk.Style()
        estilo.configure("TButton", background="lightblue", foreground="black", padding=10, font=("Arial", 10, "bold"))
        self.boton_registrar.config(style="TButton")

    def validar_numero(self, nuevo_texto):
        # Verifica si el nuevo texto es vacío o si solo contiene números
        if nuevo_texto == "" or nuevo_texto.isdigit():
            return True
        else:
            return False

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()

        # Comprobar que todos los campos son obligatorios
        if not nombre or not apellido or not direccion or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if registrar_cliente(nombre, apellido, direccion, telefono):
            messagebox.showinfo("Éxito", "Cliente registrado con éxito.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_direccion.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el cliente.")

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.crud import registrar_auto

class InterfazRegistroAuto(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear un validador que solo permite números
        vcmd_numero = (parent.register(self.validar_numero), '%P')

        # Crear los elementos de la interfaz
        ttk.Label(self, text="VIN:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_vin = ttk.Entry(self)
        self.entry_vin.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Marca:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_marca = ttk.Entry(self)
        self.entry_marca.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Modelo:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_modelo = ttk.Entry(self)
        self.entry_modelo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Año:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_anio = ttk.Entry(self, validate='key', validatecommand=vcmd_numero)
        self.entry_anio.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Precio:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_precio = ttk.Entry(self, validate='key', validatecommand=vcmd_numero)
        self.entry_precio.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Estado:").grid(row=5, column=0, padx=5, pady=5)
        self.combo_estado = ttk.Combobox(self, values=["Nuevo", "Usado"], state="readonly")  # Solo lectura
        self.combo_estado.grid(row=5, column=1, padx=5, pady=5)

        # Botón de registro con color y separación
        self.boton_registrar = ttk.Button(self, text="Registrar Auto", command=self.registrar)
        self.boton_registrar.grid(row=6, columnspan=2, pady=(20, 10))  # Añadido espacio arriba y abajo

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
        vin = self.entry_vin.get()
        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        
        # Validar que el campo Estado esté seleccionado
        estado = self.combo_estado.get()
        
        # Comprobar que todos los campos son obligatorios
        if not vin or not marca or not modelo or not self.entry_anio.get() or not self.entry_precio.get() or estado == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        try:
            anio = int(self.entry_anio.get())
            precio = float(self.entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "Año y precio deben ser números válidos.")
            return

        if registrar_auto(vin, marca, modelo, anio, precio, estado):
            messagebox.showinfo("Éxito", "Auto registrado con éxito.")
            self.entry_vin.delete(0, tk.END)
            self.entry_marca.delete(0, tk.END)
            self.entry_modelo.delete(0, tk.END)
            self.entry_anio.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
            self.combo_estado.set('')  # Reiniciar el estado
        else:
            messagebox.showerror("Error", "No se pudo registrar el auto.")

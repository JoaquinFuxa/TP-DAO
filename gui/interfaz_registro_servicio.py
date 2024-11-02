import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.crud import registrar_servicio, obtener_autos_vendidos

class InterfazRegistroServicio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear los elementos de la interfaz
        ttk.Label(self, text="Auto (VIN):").grid(row=0, column=0)
        self.combo_auto = ttk.Combobox(self)
        self.combo_auto.grid(row=0, column=1)
        self.cargar_autos()

        ttk.Label(self, text="Descripción del Servicio:").grid(row=1, column=0)
        self.entry_descripcion = ttk.Entry(self)
        self.entry_descripcion.grid(row=1, column=1)

        ttk.Label(self, text="Costo:").grid(row=2, column=0)
        self.entry_costo = ttk.Entry(self)
        self.entry_costo.grid(row=2, column=1)

        ttk.Button(self, text="Registrar Servicio", command=self.registrar).grid(row=3, columnspan=2)

    def cargar_autos(self):
        autos = obtener_autos_vendidos()
        self.combo_auto['values'] = [auto[0] for auto in autos]

    def registrar(self):
        vin = self.combo_auto.get()
        descripcion = self.entry_descripcion.get()
        costo = float(self.entry_costo.get())

        if registrar_servicio(vin, descripcion, costo):
            messagebox.showinfo("Éxito", "Servicio registrado con éxito.")
            self.combo_auto.set('')
            self.entry_descripcion.delete(0, tk.END)
            self.entry_costo.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el servicio.")

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.crud import obtener_autos_vendidos, obtener_servicios_por_auto

class InterfazConsultaServiciosAuto(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título
        ttk.Label(self, text="Consulta de Servicios de un Auto", font=("Arial", 14, "bold")).grid(row=0, columnspan=2, pady=(10, 10))

        # Selector de auto
        ttk.Label(self, text="Auto (VIN):").grid(row=1, column=0, pady=(5, 5), padx=(10, 5))
        self.combo_auto = ttk.Combobox(self, state='readonly')
        self.combo_auto.grid(row=1, column=1, pady=(5, 5), padx=(5, 10))
        self.cargar_autos()

        # Botón para mostrar servicios
        self.boton_mostrar = ttk.Button(self, text="Mostrar Servicios", command=self.mostrar_servicios)
        self.boton_mostrar.grid(row=2, columnspan=2, pady=(10, 10))

        # Tabla para mostrar servicios
        columnas = ["id_servicio", "auto", "tipo_servicio", "fecha", "costo"]
        self.treeview = ttk.Treeview(self, columns=columnas, show='headings', height=8)
        self.treeview.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10))

        # Configurar encabezados y ancho de las columnas
        col_ancho = {
            "id_servicio": 100,
            "auto": 100,
            "tipo_servicio": 120,
            "fecha": 90,
            "costo": 80
        }
        
        for col in columnas:
            self.treeview.heading(col, text=col.replace("_", " ").capitalize())
            self.treeview.column(col, anchor="center", width=col_ancho[col])

        # Estilo de los widgets
        estilo = ttk.Style()
        estilo.configure("TButton", background="lightblue", foreground="black", padding=10, font=("Arial", 10, "bold"))

    def cargar_autos(self):
        autos = obtener_autos_vendidos()
        self.combo_auto['values'] = [auto[0] for auto in autos]  # Mostrar solo el VIN

    def mostrar_servicios(self):
        vin = self.combo_auto.get()
        
        if not vin:
            messagebox.showerror("Error", "Por favor, seleccione un auto.")
            return

        # Limpiar datos anteriores en la tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Obtener servicios del auto seleccionado
        servicios = obtener_servicios_por_auto(vin)

        if servicios:
            for servicio in servicios:
                self.treeview.insert("", "end", values=servicio)
        else:
            messagebox.showinfo("Información", "No hay servicios registrados para este auto.")

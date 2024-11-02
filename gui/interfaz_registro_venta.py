import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re  # Importar el módulo de expresiones regulares
from datetime import datetime
from database.crud import registrar_venta, obtener_autos_no_vendidos, obtener_clientes, obtener_vendedores

class InterfazRegistroVenta(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Crear un validador que solo permite números
        vcmd_numero = (parent.register(self.validar_numero), '%P')

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="Auto (VIN):").grid(row=0, column=0, pady=(10, 5))
        self.combo_auto = ttk.Combobox(self, state='readonly')  # Solo selección
        self.combo_auto.grid(row=0, column=1, pady=(10, 5))
        self.cargar_autos()

        ttk.Label(self, text="Cliente:").grid(row=1, column=0, pady=(5, 5))
        self.combo_cliente = ttk.Combobox(self, state='readonly')  # Solo selección
        self.combo_cliente.grid(row=1, column=1, pady=(5, 5))
        self.cargar_clientes()

        ttk.Label(self, text="Vendedor:").grid(row=2, column=0, pady=(5, 5))
        self.combo_vendedor = ttk.Combobox(self, state='readonly')  # Solo selección
        self.combo_vendedor.grid(row=2, column=1, pady=(5, 5))
        self.cargar_vendedores()

        ttk.Label(self, text="Fecha de Venta (dd/mm/yyyy):").grid(row=3, column=0, pady=(5, 5))
        self.entry_fecha = ttk.Entry(self)  # Campo de entrada para la fecha
        self.entry_fecha.grid(row=3, column=1, pady=(5, 5))

        # Campo para el monto de la comisión
        ttk.Label(self, text="Monto de Comisión:").grid(row=4, column=0, pady=(5, 5))
        self.entry_comision = ttk.Entry(self, validate='key', validatecommand=vcmd_numero)
        self.entry_comision.grid(row=4, column=1, pady=(5, 5))

        # Botón de registro con estilo
        self.boton_registrar = ttk.Button(self, text="Registrar Venta", command=self.registrar)
        self.boton_registrar.grid(row=5, columnspan=2, pady=(20, 10))

        # Cambiar el color del botón (usando estilo)
        estilo = ttk.Style()
        estilo.configure("TButton", background="lightblue", foreground="black", padding=10, font=("Arial", 10, "bold"))
        self.boton_registrar.config(style="TButton")

    def cargar_autos(self):
        autos = obtener_autos_no_vendidos()
        self.combo_auto['values'] = [auto[0] for auto in autos]  # VIN de autos no vendidos

    def cargar_clientes(self):
        clientes = obtener_clientes()
        self.combo_cliente['values'] = [f"{cliente[0]} - {cliente[1]} {cliente[2]}" for cliente in clientes]

    def cargar_vendedores(self):
        vendedores = obtener_vendedores()
        self.combo_vendedor['values'] = [f"{vendedor[0]} - {vendedor[1]} {vendedor[2]}" for vendedor in vendedores]

    def validar_numero(self, nuevo_texto):
        # Verifica si el nuevo texto es vacío o si solo contiene números
        if nuevo_texto == "" or nuevo_texto.isdigit():
            return True
        else:
            return False

    def registrar(self):
        vin = self.combo_auto.get()
        cliente_info = self.combo_cliente.get().split(" - ")
        vendedor_info = self.combo_vendedor.get().split(" - ")
        
        cliente_id = cliente_info[0]  # Obtener el ID del cliente
        vendedor_id = vendedor_info[0]  # Obtener el ID del vendedor
        fecha = self.entry_fecha.get()  # Obtener la fecha ingresada
        comision_str = self.entry_comision.get()  # Obtener el monto de la comisión ingresado

        # Validar que todos los campos estén llenos
        if not vin or not cliente_id or not vendedor_id or not fecha or not comision_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar el formato de la fecha
        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "La fecha debe estar en formato dd/mm/yyyy.")
            return

        # Validar que el monto de la comisión sea un número
        try:
            comision = float(comision_str)
        except ValueError:
            messagebox.showerror("Error", "El monto de la comisión debe ser un número válido.")
            return

        # Registrar la venta
        if registrar_venta(vin, cliente_id, fecha, vendedor_id, comision):
            messagebox.showinfo("Éxito", "Venta registrada con éxito.")
            self.combo_auto.set('')
            self.combo_cliente.set('')
            self.combo_vendedor.set('')
            self.entry_fecha.delete(0, tk.END)  # Limpiar el campo de fecha
            self.entry_comision.delete(0, tk.END)  # Limpiar el campo de comisión
            
            # Actualizar la lista de autos disponibles
            self.cargar_autos()  # Recargar la lista de autos después de registrar la venta
            
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta.")

    def validar_fecha(self, fecha):
        # Expresión regular para validar el formato dd/mm/yyyy
        regex = r'^\d{2}/\d{2}/\d{4}$'
        if re.match(regex, fecha):
            try:
                # Intentar convertir la fecha para validar que es correcta
                dia, mes, anio = map(int, fecha.split('/'))
                datetime(anio, mes, dia)  # Si no es una fecha válida, se lanzará una excepción
                return True
            except ValueError:
                return False  # La fecha no es válida
        return False  # No coincide con el formato

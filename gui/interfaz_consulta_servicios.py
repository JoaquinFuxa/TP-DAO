from tkinter import *
from database.crud import consultar_servicios_auto

def interfaz_consultar_servicios_auto():
    ventana = Tk()
    ventana.title("Consulta de Servicios")

    Label(ventana, text="Auto (VIN)").grid(row=0)

    vin_entry = Entry(ventana)
    vin_entry.grid(row=0, column=1)

    resultados = Text(ventana)
    resultados.grid(row=2, column=0, columnspan=2)

    def consultar():
        vin = vin_entry.get()
        servicios = consultar_servicios_auto(vin)
        resultados.delete('1.0', END)  # Limpiar resultados previos
        for servicio in servicios:
            resultados.insert(END, f"Tipo: {servicio[0]}, Fecha: {servicio[1]}, Costo: {servicio[2]}\n")

    Button(ventana, text="Consultar", command=consultar).grid(row=1, column=1)

    ventana.mainloop()

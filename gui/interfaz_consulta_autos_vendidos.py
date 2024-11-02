from tkinter import *
from database.crud import consultar_autos_vendidos

def interfaz_consultar_autos_vendidos():
    ventana = Tk()
    ventana.title("Consulta de Autos Vendidos")

    Label(ventana, text="Cliente (ID)").grid(row=0)

    cliente_id_entry = Entry(ventana)
    cliente_id_entry.grid(row=0, column=1)

    resultados = Text(ventana)
    resultados.grid(row=2, column=0, columnspan=2)

    def consultar():
        cliente_id = cliente_id_entry.get()
        autos_vendidos = consultar_autos_vendidos(cliente_id)
        resultados.delete('1.0', END)  # Limpiar resultados previos
        for auto in autos_vendidos:
            resultados.insert(END, f"VIN: {auto[0]}, Marca: {auto[1]}, Modelo: {auto[2]}, Año: {auto[3]}\n")

    Button(ventana, text="Consultar", command=consultar).grid(row=1, column=1)

    ventana.mainloop()

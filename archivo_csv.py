import csv
import os

def guardar_puntaje(nombre, puntaje):
    ruta = "puntajes.csv"

    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("Nombre,Puntaje\n")

    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(nombre + "," + str(puntaje) + "\n")
        

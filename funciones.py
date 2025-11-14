import json
import random

def menu():
    print(f"================================")
    print("MINI GENERALA ")
    print(f"================================")
    print("1. jugar ")
    print("2. Estadísticas ")
    print("3. Créditos ")
    print("4. Salir ")
    
    opcion = input("Ingrese una opción: ")
    while not opcion.isdigit() or opcion not in ("1", "2", "3", "4"):
        print("Error, ingrese una opción y caracter válido...")
        opcion = input("Ingrese una opción: ")
    return opcion

def main():
    opcion = ""
    while opcion != "4":
        opcion = menu()
        if opcion == "1":
            empezar_juego()
            pass
        elif opcion == "2":
            mostrar_estadisticas()
            pass
        elif opcion == "3":
            mostrar_creditos()
            pass
        elif opcion == "4":
            print("Gracias por jugar!! ")
            break

def empezar_juego():
    print("Iniciando juego... ")

    nivel = cargar_nivel()
    planilla = cargar_planilla(nivel)
    total = 0

    while not juego_terminado(planilla):
        print("\n==============================")
        print(f"PUNTAJE TOTAL: {total}")
        print("================================")

        mostrar_planilla(planilla)

        dados = turno_de_tiros(nivel)

        categoria = elegir_categoria(planilla)

        puntos = calcular_puntaje(categoria, dados, nivel)
        planilla[categoria] = puntos
        total += puntos

        print(f"\nAnotaste {puntos} puntos en {categoria}! ")
    
    print("JUEGO TERMINADO ")
    print(f"Puntaje final: {total} ")
    pass

def cargar_nivel():
    return {
        "tematica": ["JEDI", "SITH", "NAVE", "DROID", "CLON", "MAESTRO"],
        "categorias" : {
            "escalera" : 20,
            "full" : 30,
            "poker" : 40,
            "generala" : 50
        }
    }


def crear_planilla(planilla):
    return {
        "Escalera" : None,
        "Full" : None,
        "poker" : None,
        "generala" : None 
    }

def juego_terminado(planilla):
    for categoria in planilla:
        if planilla[categoria] == None:
            return False
    return True

def mostrar_planilla(planilla):
    print(f"\nPLANILLA ")
    for categoria, puntos in planilla.items():
        if puntos == None:
            texto = "-"
        else:
            texto = puntos
        print(f"{categoria}: {texto} ")


def turno_de_tiros(nivel):
    print("\n---TIRANDO LOS DADOS---")
    dados = tirar_dados()
    print(f"Primer tiro: {representar_dados(dados, nivel)} ")
    return dados

def tirar_dados():
    dados = []
    for i in range(5):
        numero = random.randint(1,6)
        dados.append(numero)
    return dados

def representar_dados(dados, nivel):
    tematica = nivel["tematica"]
    representacion = []

    for x in dados:
        palabra = tematica[x-1]
        representacion.append(palabra)
    
    return representacion


def elegir_categoria(planilla):
    print(f"--- Elegí una categoría --- ")
    categorias_libres = []
    numero = 1

    for categoria in planilla.keys():
        if planilla[categoria] == None:
            print(f"{numero} . {categoria} ")
            categorias_libres.append(categoria)
            numero += 1
    
    opcion = input("Opción: ")
    while not opcion.isdigit():
        opcion = input("Opción: ")
    
    opcion = int(opcion)
    return categorias_libres[opcion-1]


def calcular_puntaje(categoria, dados, nivel):
    return len(set(dados))



def mostrar_estadisticas():
    print("Cargando estadísticas...")
    pass

def mostrar_creditos():
    print("Cargando créditos...")
    pass

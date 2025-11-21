import json
import random
import copy

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


def menu():
    print(f"========================")
    print("\t   MINI GENERALA ")
    print(f"========================")
    print("1. jugar ")
    print("2. Estadísticas ")
    print("3. Créditos ")
    print("4. Salir ")
    
    opcion = input("Ingrese una opción: ")
    while not opcion.isdigit() or opcion not in ("1", "2", "3", "4"):
        print("Error, ingrese una opción y caracter válido...")
        opcion = input("Ingrese una opción: ")
    return opcion



def empezar_juego():
    print("Iniciando juego... ")

    nivel = cargar_nivel()
    planilla = cargar_planilla(nivel)
    terminado = False

    while not terminado:

        mostrar_planilla(planilla)

        dados_finales = turno_de_tiros(nivel)

        print("Dados finales del turno: ")
        print(representar_dados(dados_finales, nivel))


        categoria = elegir_categoria(planilla)
        print(f"Elegiste la categoría: {categoria} ")


        #puntaje aún no implementado
        planilla[categoria] = calcular_puntaje(categoria, dados_finales)

        terminado = juego_terminado(planilla)

        

        
    
    print("JUEGO TERMINADO ")
    #print(f"Puntaje final: {total} ")
    pass


def cargar_nivel():
    nivel = {
        "tematica" : ["1", "2", "3", "4", "5", "6"]
    }
    return nivel


def cargar_planilla(nivel):

    planilla = {
        "1" : None,
        "2" : None,
        "3" : None,
        "4" : None,
        "5" : None,
        "6" : None,
        "Escalera" : None,
        "Full" : None,
        "Poker" : None,
        "Generala" : None
    }
    return planilla

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


def tirar_dados():
    lista = []
    for i in range(5):
        lista.append(random.randint(1,6))
    return lista



def representar_dados(dados, nivel):
    tematica = nivel["tematica"]
    resultado = []
    for x in dados:
        resultado.append(tematica[x-1])
    return resultado



def turno_de_tiros(nivel):
    dados = tirar_dados()
    print(f"--- PRIMER TIRO --- ")
    print(representar_dados(dados, nivel))

    tiradas = 1

    while tiradas < 3:
        respuesta = input(f"Desea volver a tirar los dados? (s/n) ").lower()
        while respuesta not in ("s", "n"):
            respuesta = input(f"Desea volver a tirar los dados? (s/n) ")
        
        if respuesta == "n":
            break

        guardados = elegir_dados_a_guardar(dados)

        cant_a_tirar = 5 - len(guardados)
        nuevos = []

        for x in range(cant_a_tirar):
            nuevos.append(random.randint(1,6))

        dados = guardados + nuevos

        tiradas += 1
        print(f"Tiro n° {tiradas}: {representar_dados(dados, nivel)} ")
    return dados



def elegir_dados_a_guardar(dados):
    print(f"Dados actuales: ")
    for x in range(len(dados)):
        print(f"{x+1}) {dados[x]} ")
    
    while True:
        eleccion = input("Escriba los dados que quiera guardar (ejemplo: 3, 5, 1): ")
        posiciones = eleccion.split()

        dados_guardados = []
        
        for pos in posiciones:
            if pos.isdigit():
                pos = int(pos)
                if 1 <= pos <= len(dados):
                    if dados[pos -1] not in dados_guardados:
                        dados_guardados.append(dados[pos-1])
        if len(dados_guardados) == 0:
            print("\nNo elegiste ninguna opción válida. Volvé a seleccionar: ")
            continue

        print(f"Elegiste guardar estos dados: {dados_guardados} ")

        confirmacion = input("Confirmas la elección? (s/n) ").lower()

        while confirmacion not in ("s", "n"):
            confirmacion = input("Confirmas la elección? (s/n) ").lower()
        
        if confirmacion == "s":
            return dados_guardados
        
        print("\nVolvé a elegir los dados\n ")



def elegir_categoria(planilla):
    print("\n--- Elegí una categoría: ---")
    categorias_libres = []
    numero = 1

    for categoria in planilla.keys():
        if planilla[categoria] == None:
            print(f"{numero}. {categoria} ")
            categorias_libres.append(categoria)
            numero += 1
    
    opcion = input("Opción: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(categorias_libres):
        opcion = input("Error. Ingresá una opción valida: ")

    opcion = int(opcion)
    
    return categorias_libres[opcion - 1]



def calcular_puntaje(categoria, dados):
    if categoria.isdigit():
        numero = int(categoria)
        total = 0

        for d in dados:
            if d == numero:
                total += d
            
        return total
    
    contador = {}

    for d in dados:
        if d not in contador:
            contador[d] = 1
        else:
            contador[d] += 1

    
    if categoria.lower() == "generala":
        for cantidad in contador.values():
            if cantidad == 5:
                return 50
        return 0
    
    if categoria.lower() == "full":
        tiene3 = False
        tiene2 = False

        for cantidad in contador.values():
            if cantidad == 3:
                tiene3 = True
            elif cantidad == 2:
                tiene2 = True
            
        if tiene3 and tiene2:
            return 30
        
        return 0
    

    if categoria.lower() == "escalera":
        ordenados = copy.copy(dados)
        ordenados.sort()

        if ordenados == [1,2,3,4,5] or ordenados == [2,3,4,5,6]:
            return 20
        
        return 0
    

    if categoria.lower() == "poker":

        for cantidad in contador.values():
            if cantidad == 4:
                return 40
            
        return 0
    return 0



def mostrar_estadisticas():
    print("Cargando estadísticas...")
    pass



def mostrar_creditos():
    print("Cargando créditos...")
    pass






















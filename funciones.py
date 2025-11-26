import json
import random
import copy
import os
from archivo_csv import guardar_puntaje as gp


def main():
    opcion = ""
    while opcion != "5":
        opcion = menu()
        if opcion == "1":
            empezar_juego()
        elif opcion == "2":
            mostrar_estadisticas()
        elif opcion == "3":
            mostrar_creditos()
        elif opcion == "4":
            mostrar_reglas()
        elif opcion == "5":
            print("Gracias por jugar!! ")
            break


def menu():
    print(f"========================")
    print("      MINI GENERALA ")
    print(f"========================")
    print("1. jugar ")
    print("2. Estadísticas ")
    print("3. Créditos ")
    print("4. Mostrar reglas ")
    print("5. Salir ")
    
    opcion = input("Ingrese una opción: ")
    while not opcion.isdigit() or opcion not in ("1", "2", "3", "4", "5"):
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

        resultado_tiros = turno_de_tiros(nivel)
        if resultado_tiros == "GANO_SERVIDA":
            print("GANÓ LA GENERALA AL PRIMER TIRO!! GENERALA SERVIDA!")
            total = 100

            print(f"Puntaje final: {total} \n")
            guardar_partida(total)
            return
    
        dados_finales = resultado_tiros


        print("Dados finales del turno: ")
        print(representar_dados(dados_finales, nivel)) 

        

        categoria = elegir_categoria(planilla, dados_finales, nivel)
        print(f"Elegiste la categoría: {categoria} ")

        puntos_obtenidos = calcular_puntaje(categoria, dados_finales, nivel)
        planilla[categoria] = puntos_obtenidos

        print(f"Obtuviste {puntos_obtenidos} puntos en {categoria} ")

        terminado = juego_terminado(planilla)

        
    print("JUEGO TERMINADO \n")
    
    total = 0
    for categoria in planilla:
        total = total + planilla[categoria]

    print(f"Puntaje final: {total} \n")
    guardar_partida(total)



def guardar_partida(total):
    nombre = input("Ingrese su nombre: ")
    gp(nombre, total)
    print("\nPuntaje guardado con exito\n")


def cargar_nivel():
    ruta = "niveles.json"
    with open(ruta, "r", encoding="utf-8") as archivo:
        nivel = json.load(archivo)
    return nivel


def cargar_planilla(nivel):
    planilla = {}
    
    for clave in nivel["categorias"]:
        nombre_categoria = nivel["categorias"][clave]
        planilla[nombre_categoria] = None

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
    if es_generala(dados):
        eleccion = input("SACASTE GENERALA SERVIDA!! Querés declararte ganador YA? (s/n) ").lower()
        while eleccion not in ("s", "n"):
            eleccion = input("SACASTE GENERALA SERVIDA!! Querés declararte ganador YA? (s/n) ").lower()
        if eleccion == "s":
            return "GANO_SERVIDA"
    

    tiradas = 1

    while tiradas < 3:
        respuesta = input(f"Desea volver a tirar los dados? (s/n) ").lower()
        while respuesta not in ("s", "n"):
            respuesta = input(f"Desea volver a tirar los dados? (s/n) ")
        
        if respuesta == "n":
            break

        dados = elegir_dados_a_guardar(dados)

        cant_a_tirar = 5 - len(dados)
        nuevos = []

        for x in range(cant_a_tirar):
            nuevos.append(random.randint(1,6))

        dados = dados + nuevos

        tiradas += 1
        print(f"Tiro n° {tiradas}: {representar_dados(dados, nivel)} ")
    return dados


def es_generala(dados):
    primer_dado = dados[0]
    for dado in dados:
        if dado != primer_dado:
            return False
    return True



def elegir_dados_a_guardar(dados):
    print(f"Dados actuales: ")
    for x in range(len(dados)):
        print(f"{x+1}) {dados[x]} ")
    
    while True:
        eleccion = input("Escriba las POSICIONES de los dados a guardar (ejemplo: 3, 5, 1): ")
        posiciones = eleccion.split()

        indices_usados = []
        dados_guardados = []
        
        for pos in posiciones:
            if not pos.isdigit():
                dados_guardados = []
                break

            indice = int(pos) -1

            if indice < 0 or indice >= len(dados) or indice in indices_usados:
                dados_guardados = []
                break

            indices_usados.append(indice)
            dados_guardados.append(dados[indice])
                

        if len(dados_guardados) != len(posiciones) or len(dados_guardados)== 0:
            print("\nNo elegiste ninguna opción válida. Volvé a seleccionar: ")
            continue

        print(f"Elegiste guardar estos dados: {dados_guardados} ")

        confirmacion = input("Confirmas la elección? (s/n) ").lower()

        while confirmacion not in ("s", "n"):
            confirmacion = input("Confirmas la elección? (s/n) ").lower()
        
        if confirmacion == "s":
            return dados_guardados
        
        print("\nVolvé a elegir los dados\n ")



def elegir_categoria(planilla, dados_finales, nivel):
    while True:
        print("\n--- Elegí una categoría: ---")
        categorias_libres = []
        numero = 1

        lista_categorias = list(planilla.keys())

        for categoria in lista_categorias:
            if planilla[categoria] == None:
                puntaje_potencial = calcular_puntaje(categoria, dados_finales, nivel)
                print(f"{numero}. {categoria} -> {puntaje_potencial} puntos")
                categorias_libres.append(categoria)
                numero += 1
    
        opcion = input("Opción: ")
        while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(categorias_libres):
            opcion = input("Error. Ingresá una opción valida: ")

        opcion_int = int(opcion)
        categoria_final = categorias_libres[opcion_int - 1]

        print(f"\nSeleccionaste: {categoria_final}")
        confirmacion = input("Desea confirmar esta elección? (s/n) ").lower()
        while confirmacion not in ("s", "n"):
            confirmacion = input("Desea confirmar esta elección? (s/n) ").lower()
        if confirmacion == "s":
            return categoria_final
        else:
            print("Voliendo a elección de categorías...")



def calcular_puntaje(categoria, dados, nivel):

    clave_identificada = ""
    for tipo, nombre in nivel["categorias"].items():
        if nombre == categoria:
            clave_identificada = tipo
            break

    if clave_identificada.isdigit():
        numero_buscado = int(clave_identificada)
        total = 0

        for d in dados:
            if d == numero_buscado:
                total += d
            
        return total
    
    contador = {}

    for d in dados:
        if d not in contador:
            contador[d] = 1
        else:
            contador[d] += 1

    
    if clave_identificada == "Generala":
        for cantidad in contador.values():
            if cantidad == 5:
                return 50
        return 0
    
    if clave_identificada == "Full":
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
    

    if clave_identificada == "Escalera":
        ordenados = copy.copy(dados)
        ordenados.sort()

        if ordenados == [1,2,3,4,5] or ordenados == [2,3,4,5,6]:
            return 20
        
        return 0
    

    if clave_identificada == "Poker":

        for cantidad in contador.values():
            if cantidad == 4 or cantidad == 5:
                return 40
            
        return 0
    return 0



def mostrar_estadisticas():
    ruta = "puntajes.csv"

    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        print("\nNo hay estadísticas registradas aún ")
        return
    
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    
    if len(lineas) <= 1:
        print("\nTodavía no hay puntajes cargados ")
        return

    puntajes = []
    
    for linea in lineas[1:]:
        linea = linea.strip().split(",")
        nombre = linea[0]
        puntaje = int(linea[1])
        puntajes.append([puntaje, nombre])
        

    puntajes.sort()
    puntajes.reverse()

    print("\n-----RANKING TOP 10-----")

    contador = 0
    for jugador in puntajes:
        if contador == 10:
            break
        print(str(contador + 1) + ". " + jugador[1] + " - " + str(jugador[0]))
        contador += 1


def mostrar_reglas():
    nivel = cargar_nivel()

    reglas_categorias = nivel["categorias"]

    print("\n" + "=" * 40)
    print("      REGLAS DE LA GENERALA TEMÁTICA    ")
    print("=" * 40)


    print("--- Categorías Numéricas (Suman el valor de los dados): ---")
    print(f" * {reglas_categorias['1']}: Suma los dados con valor 1.")
    print(f" * {reglas_categorias['2']}: Suma los dados con valor 2.")
    print(f" * {reglas_categorias['3']}: Suma los dados con valor 3.")
    print(f" * {reglas_categorias['4']}: Suma los dados con valor 4.")
    print(f" * {reglas_categorias['5']}: Suma los dados con valor 5.")
    print(f" * {reglas_categorias['6']}: Suma los dados con valor 6.")

    print("\n--- Categorías Especiales (Patrones): ---")

    print(f" * {reglas_categorias['Escalera']} (20 pts): Secuencia de 5 dados (1-2-3-4-5 o 2-3-4-5-6).")

    print(f" * {reglas_categorias['Full']} (30 pts): Tres dados iguales y otros dos iguales.")

    print(f" * {reglas_categorias['Poker']} (40 pts): Cuatro dados iguales.")

    print(f" * {reglas_categorias['Generala']} (50 pts): Cinco dados iguales.")
    print(f"   (Servida: Si es en el primer tiro, la Generala suma 100 puntos y gana la partida).")

    print("=" * 40)
    input("Presione ENTER para volver al menú...")
    return





def mostrar_creditos():
    print("Cargando créditos...")
    print( "Lisandro Nuñez - codigo de juego\n")






















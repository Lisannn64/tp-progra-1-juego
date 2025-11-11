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
            #empezar_juego()
            pass
        elif opcion == "2":
            #mostrar_estadisticas()
            pass
        elif opcion == "3":
            #mostrar_creditos()
            pass
        elif opcion == "4":
            print("Gracias por jugar!! ")
            break

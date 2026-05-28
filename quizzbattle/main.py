from services.autenticacio import iniciar_sessio
from services.registre import registrar_usuari

def mostrar_menu():
    usuari_actiu = None
    while True:
        print()
        print("        MENÚ PRINCIPAL       ")
        print()
        print("1. Registre usuari")
        print("2. Iniciar sessió")
        print("3. Importar qüestionari")
        print("4. Jugar qüestionari (individual)")
        print("5. Mode 1 vs 1")
        print("6. Consultar estadístiques personals")
        print("7. Consultar estadístiques qüestionari")
        print("8. Consultar rànquing global")
        print("9. Sortir")

        opcio = input("Selecciona una opció: ")

        match opcio:
            case "1":
                registrar_usuari()

            case "2":
                usuari_actiu = iniciar_sessio()

            case "3":
                print(" Importa un questionari  ")

            case "4":
                print(" Juga al questionari en solitari ")

            case "5":
                print(" Juga mode 1 vs 1    ")

            case "6":
                print(" Estadístiques personals ")

            case "7":
                print(" Estadístiques questionaris  ")

            case "8":
                print(" RANKING GLOBAL  ")

            case "9":
                print(" SORTINT DEL PROGRAMA    ")
                break

            case _:
                print(" Opció no valida    ")


mostrar_menu()

import os
import sys

# Afegir el directori pare al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quizzbattle.services.importacio_json import JSONImporter


def importar_questionari():
    importer = JSONImporter()
    nom_fitxer = "questionaris_prova.json"

    # Si no és path absolut, busca a la carpeta data/
    if not os.path.isabs(nom_fitxer) and not os.path.exists(nom_fitxer):
        ruta = os.path.join(os.path.dirname(__file__), 'data', nom_fitxer)
    else:
        ruta = nom_fitxer

    questionaris = importer.importar_questionaris(ruta)

    if questionaris:
        print(f"\nS'han importat {importer.get_num_questionaris_importats()} qüestionari(s):\n")
        for q in questionaris:
            print(f"  Títol     : {q.get_titol()}")
            print(f"  Categoria : {q.get_categoria()}")
            print(f"  Dificultat: {q.get_dificultat()}/5")
            print(f"  Preguntes : {len(q.get_preguntes())}")
            for p in q.get_preguntes():
                print(f"    [{p.get_tipus()}] {p.get_enunciat()} ({p.get_punts()} pt)")
            print()
    else:
        print("No s'ha pogut importar cap qüestionari.")

    return questionaris


def main():
    print("=" * 45)
    print("        BENVINGUT A QUIZZBATTLE")
    print("=" * 45)

    while True:
        print("\nMENÚ PRINCIPAL")
        print("  1. Registre usuari")
        print("  2. Iniciar sessió")
        print("  3. Importar qüestionari (demo sense BD)")
        print("  4. Sortir")
        opcio = input("\nTria una opció: ").strip()

        if opcio == '3':
            importar_questionari()
        elif opcio == '4':
            print("Fins aviat!")
            break
        else:
            print("(Opció no implementada encara)")


if __name__ == "__main__":
    main()

import random
from database.database import get_connection, finalitzar_questionari, guardar_partida_vs
from models.questionari import Questionari
from models.pregunta import Pregunta
from services.autenticacio import iniciar_sessio

def jugar_questionari_individual(usuari_actiu):
    if not usuari_actiu:
        print("Debes iniciar sesión para jugar un cuestionario individual.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_questionari, titol, categoria, dificultat FROM questionaris")
        questionaris_db = cursor.fetchall()

        if not questionaris_db:
            print("No hay cuestionarios disponibles. Por favor, importa uno primero.")
            return

        print("\n--- Cuestionarios Disponibles ---")
        for q in questionaris_db:
            print(f"{q[0]}. {q[1]} ({q[2]} - {q[3]})")

        while True:
            try:
                seleccion = int(input("Selecciona el ID del cuestionario que quieres jugar: "))
                if any(q[0] == seleccion for q in questionaris_db):
                    break
                else:
                    print("ID de cuestionario no válido. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número.")

        cursor.execute("SELECT id_pregunta, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts FROM preguntes WHERE id_questionari = %s", (seleccion,))
        preguntas_db = cursor.fetchall()

        if not preguntas_db:
            print("El cuestionario seleccionado no tiene preguntas.")
            return

        preguntas = []
        for p in preguntas_db:
            preguntas.append(Pregunta(p[0], seleccion, p[1], p[2], p[3], p[4], p[5], p[6], p[7]))

        respostes_correctes = 0
        respostes_errades = 0
        punts_obtinguts = 0
        punts_totals = 0

        for i, pregunta in enumerate(preguntas):
            print(f"\n--- Pregunta {i+1} ---")
            print(pregunta.get_enunciat())
            opciones = [pregunta.get_resposta1(), pregunta.get_resposta2(), pregunta.get_resposta3(), pregunta.get_resposta4()]
            random.shuffle(opciones)
            for j, opcion in enumerate(opciones):
                print(f"{j+1}. {opcion}")

            while True:
                try:
                    respuesta_usuario = int(input("Tu respuesta (número): "))
                    if 1 <= respuesta_usuario <= len(opciones):
                        break
                    else:
                        print("Opción no válida. Introduce un número entre 1 y 4.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número.")
            
            punts_totals += pregunta.get_punts()
            if opciones[respuesta_usuario - 1] == pregunta.get_resposta_correcta():
                print("¡Respuesta correcta!")
                respostes_correctes += 1
                punts_obtinguts += pregunta.get_punts()
            else:
                print(f"Respuesta incorrecta. La respuesta correcta era: {pregunta.get_resposta_correcta()}")
                respostes_errades += 1

        resultados = finalitzar_questionari(conn, seleccion, usuari_actiu.get_id_usuari(), respostes_correctes, respostes_errades, punts_obtinguts, punts_totals)
        print("\n--- Resumen del Juego ---")
        print(f"Encuestas correctas: {resultados['encerts']}")
        print(f"Encuestas incorrectas: {resultados['errades']}")
        print(f"Puntuación final: {resultados['puntuacio_final']}")

    except Exception as e:
        print(f"Ocurrió un error durante el juego: {e}")
    finally:
        conn.close()

def jugar_questionari_1vs1(usuari_actiu):
    if not usuari_actiu:
        print("Debes iniciar sesión para jugar en modo 1 vs 1.")
        return

    print("\n--- Modo 1 vs 1 ---")
    print("Jugador 1: ", usuari_actiu.get_nom_usuari())

    print("\nIntroduce los datos del Jugador 2:")
    usuari2 = iniciar_sessio()
    if not usuari2:
        print("No se pudo iniciar sesión para el Jugador 2. Cancelando partida.")
        return
    
    if usuari_actiu.get_id_usuari() == usuari2.get_id_usuari():
        print("No puedes jugar contra ti mismo. Por favor, selecciona otro usuario para el Jugador 2.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_questionari, titol, categoria, dificultat FROM questionaris")
        questionaris_db = cursor.fetchall()

        if not questionaris_db:
            print("No hay cuestionarios disponibles. Por favor, importa uno primero.")
            return

        print("\n--- Cuestionarios Disponibles ---")
        for q in questionaris_db:
            print(f"{q[0]}. {q[1]} ({q[2]} - {q[3]})")

        while True:
            try:
                seleccion = int(input("Selecciona el ID del cuestionario que quieren jugar: "))
                if any(q[0] == seleccion for q in questionaris_db):
                    break
                else:
                    print("ID de cuestionario no válido. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número.")

        cursor.execute("SELECT id_pregunta, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts FROM preguntes WHERE id_questionari = %s", (seleccion,))
        preguntas_db = cursor.fetchall()

        if not preguntas_db:
            print("El cuestionario seleccionado no tiene preguntas.")
            return

        preguntas = []
        for p in preguntas_db:
            preguntas.append(Pregunta(p[0], seleccion, p[1], p[2], p[3], p[4], p[5], p[6], p[7]))

        respostes_correctes_j1 = 0
        respostes_errades_j1 = 0
        punts_obtinguts_j1 = 0

        respostes_correctes_j2 = 0
        respostes_errades_j2 = 0
        punts_obtinguts_j2 = 0

        punts_totals_cuestionario = 0

        for i, pregunta in enumerate(preguntas):
            print(f"\n--- Pregunta {i+1} ---")
            print(pregunta.get_enunciat())
            opciones = [pregunta.get_resposta1(), pregunta.get_resposta2(), pregunta.get_resposta3(), pregunta.get_resposta4()]
            random.shuffle(opciones)
            for j, opcion in enumerate(opciones):
                print(f"{j+1}. {opcion}")

            punts_totals_cuestionario += pregunta.get_punts()

            while True:
                try:
                    respuesta_j1 = int(input(f"Jugador 1 ({usuari_actiu.get_nom_usuari()}), tu respuesta (número): "))
                    if 1 <= respuesta_j1 <= len(opciones):
                        break
                    else:
                        print("Opción no válida. Introduce un número entre 1 y 4.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número.")
            
            if opciones[respuesta_j1 - 1] == pregunta.get_resposta_correcta():
                print("Jugador 1: ¡Respuesta correcta!")
                respostes_correctes_j1 += 1
                punts_obtinguts_j1 += pregunta.get_punts()
            else:
                print(f"Jugador 1: Respuesta incorrecta. La respuesta correcta era: {pregunta.get_resposta_correcta()}")
                respostes_errades_j1 += 1

            while True:
                try:
                    respuesta_j2 = int(input(f"Jugador 2 ({usuari2.get_nom_usuari()}), tu respuesta (número): "))
                    if 1 <= respuesta_j2 <= len(opciones):
                        break
                    else:
                        print("Opción no válida. Introduce un número entre 1 y 4.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número.")

            if opciones[respuesta_j2 - 1] == pregunta.get_resposta_correcta():
                print("Jugador 2: ¡Respuesta correcta!")
                respostes_correctes_j2 += 1
                punts_obtinguts_j2 += pregunta.get_punts()
            else:
                print(f"Jugador 2: Respuesta incorrecta. La respuesta correcta era: {pregunta.get_resposta_correcta()}")
                respostes_errades_j2 += 1

        resultados_vs = guardar_partida_vs(conn, seleccion, usuari_actiu.get_id_usuari(), usuari2.get_id_usuari(),
                                           punts_obtinguts_j1, punts_totals_cuestionario,
                                           punts_obtinguts_j2, punts_totals_cuestionario)

        print("\n--- Resumen del Juego 1 vs 1 ---")
        print(f"Jugador 1 ({usuari_actiu.get_nom_usuari()}): ")
        print(f"  Encuestas correctas: {respostes_correctes_j1}")
        print(f"  Encuestas incorrectas: {respostes_errades_j1}")
        print(f"  Puntuación final: {resultados_vs['puntuacio1']}")
        print(f"  Resultado: {resultados_vs['resultat1']}")

        print(f"\nJugador 2 ({usuari2.get_nom_usuari()}): ")
        print(f"  Encuestas correctas: {respostes_correctes_j2}")
        print(f"  Encuestas incorrectas: {respostes_errades_j2}")
        print(f"  Puntuación final: {resultados_vs['puntuacio2']}")
        print(f"  Resultado: {resultados_vs['resultat2']}")

        if resultados_vs['resultat1'] == 'WIN':
            print(f"\n¡El ganador es el Jugador 1 ({usuari_actiu.get_nom_usuari()})!")
        elif resultados_vs['resultat2'] == 'WIN':
            print(f"\n¡El ganador es el Jugador 2 ({usuari2.get_nom_usuari()})!")
        else:
            print("\n¡Es un empate!")

    except Exception as e:
        print(f"Ocurrió un error durante el juego 1 vs 1: {e}")
    finally:
        conn.close()
import json
from ..models.questionari import Questionari
from ..models.pregunta import PreguntaVF, PreguntaMultiple
from database.database import get_connection, insert_questionari_db, insert_pregunta_db, get_questionari_by_title_and_owner_db, update_questionari_db, delete_preguntes_by_questionari_id

class JSONImporter:
    def __init__(self):
        self.questionaris_importats = []

    def importar_questionaris(self, file_path, usuari_actiu):
        if not usuari_actiu:
            print("Debes iniciar sesión para importar cuestionarios.")
            return 0, 0

        id_propietari = usuari_actiu["id_usuari"]
        created_count = 0
        updated_count = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: No se ha encontrado el archivo '{file_path}'.")
            return 0, 0
        except json.JSONDecodeError as e:
            print(f"Error de formato JSON: {e}")
            return 0, 0
        except Exception as e:
            print(f"Error leyendo el archivo: {e}")
            return 0, 0

        conn = get_connection()
        try:
            for quiz_data in data.get('questionaris', []):
                if 'informacio' in quiz_data:
                    info = quiz_data['informacio']
                else:
                    info = quiz_data

                titol = info.get('titol', 'Sense títol')
                categoria = info.get('categoria', '')
                dificultat = info.get('dificultat', 1)
                descripcio = info.get('descripcio', '')

                # Comprobar si ya existe un cuestionario con el mismo título y propietario
                existing_questionari_data = get_questionari_by_title_and_owner_db(conn, titol, id_propietari)

                if existing_questionari_data:
                    print(f"\nEl cuestionario '{titol}' ya existe. ¿Qué deseas hacer?")
                    print("1. Actualizarlo")
                    print("2. Guardarlo con un nuevo título")
                    choice = input("Selecciona una opción (1/2): ")

                    if choice == '1':
                        # Actualizar cuestionario existente
                        q_obj = Questionari(existing_questionari_data['id_questionari'], id_propietari, titol, categoria, dificultat, descripcio)
                        update_questionari_db(conn, q_obj, existing_questionari_data['id_questionari'])
                        delete_preguntes_by_questionari_id(conn, existing_questionari_data['id_questionari'])
                        id_questionari_actual = existing_questionari_data['id_questionari']
                        updated_count += 1
                        print(f"Cuestionario '{titol}' actualizado.")
                    elif choice == '2':
                        # Guardar con nuevo título
                        new_titol = input(f"Introduce un nuevo título para '{titol}': ")
                        q_obj = Questionari(None, id_propietari, new_titol, categoria, dificultat, descripcio)
                        id_questionari_actual = insert_questionari_db(conn, q_obj, id_propietari)
                        created_count += 1
                        print(f"Cuestionario '{titol}' guardado con el nuevo título '{new_titol}'.")
                    else:
                        print("Opción no válida. Se omite la importación de este cuestionario.")
                        continue
                else:
                    # Insertar nuevo cuestionario
                    q_obj = Questionari(None, id_propietari, titol, categoria, dificultat, descripcio)
                    id_questionari_actual = insert_questionari_db(conn, q_obj, id_propietari)
                    created_count += 1
                    print(f"Cuestionario '{titol}' importado.")

                # Insertar preguntas
                for p_data in quiz_data.get('preguntes', []):
                    enunciat = p_data.get('enunciat', '')
                    resposta_correcta_idx = p_data.get('resposta_correcta', 1)
                    punts = p_data.get('punts', 1)
                    tipus = p_data.get('tipus', '').lower()

                    if 'respostes' in p_data and isinstance(p_data['respostes'], dict):
                        respostes = p_data['respostes']
                        r1 = respostes.get('resposta1')
                        r2 = respostes.get('resposta2')
                        r3 = respostes.get('resposta3')
                        r4 = respostes.get('resposta4')
                    else:
                        r1 = p_data.get('resposta1')
                        r2 = p_data.get('resposta2')
                        r3 = p_data.get('resposta3')
                        r4 = p_data.get('resposta4')

                    if tipus in ('vf', 'verdader/fals', 'verdader_fals'):
                        p_obj = PreguntaVF(None, id_questionari_actual, enunciat, r1 or 'Verdader', r2 or 'Fals', resposta_correcta_idx, punts)
                    else:
                        p_obj = PreguntaMultiple(None, id_questionari_actual, enunciat, r1, r2, r3, r4, resposta_correcta_idx, punts)
                    
                    insert_pregunta_db(conn, p_obj, id_questionari_actual)

        except Exception as e:
            print(f"Ocurrió un error durante la importación: {e}")
        finally:
            conn.close()

        return created_count, updated_count
import json
from quizzbattle.models.questionari import Questionari
from quizzbattle.models.pregunta import PreguntaVF, PreguntaMultiple


class JSONImporter:
    def __init__(self):
        self.questionaris_importats = []

    def importar_questionaris(self, file_path, id_propietari=1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: No s'ha trobat el fitxer '{file_path}'.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error de format JSON: {e}")
            return []
        except Exception as e:
            print(f"Error llegint el fitxer: {e}")
            return []

        imported_objects = []
        id_questionari_counter = 1
        id_pregunta_counter = 1

        for quiz_data in data.get('questionaris', []):
            # Suporta tant estructura plana com amb subobjete 'informacio'
            if 'informacio' in quiz_data:
                info = quiz_data['informacio']
            else:
                info = quiz_data

            id_q = info.get('id_questionari', id_questionari_counter)
            titol = info.get('titol', 'Sense títol')
            categoria = info.get('categoria', '')
            dificultat = info.get('dificultat', 1)
            descripcio = info.get('descripcio', '')

            q = Questionari(id_q, id_propietari, titol, categoria, dificultat, descripcio)

            for p_data in quiz_data.get('preguntes', []):
                id_p = p_data.get('id_pregunta', id_pregunta_counter)
                id_q_ref = p_data.get('id_questionari', id_q)
                enunciat = p_data.get('enunciat', '')
                resposta_correcta = p_data.get('resposta_correcta', 1)
                punts = p_data.get('punts', 1)
                tipus = p_data.get('tipus', '').lower()

                # Suporta respostes com a subobjete {'resposta1': ..., ...} o camps plans
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
                    p = PreguntaVF(id_p, id_q_ref, enunciat, r1 or 'Verdader', r2 or 'Fals', resposta_correcta, punts)
                else:
                    p = PreguntaMultiple(id_p, id_q_ref, enunciat, r1, r2, r3, r4, resposta_correcta, punts)

                q.add_pregunta(p)
                id_pregunta_counter += 1

            imported_objects.append(q)
            self.questionaris_importats.append(q)
            id_questionari_counter += 1

        return imported_objects

    def get_num_questionaris_importats(self):
        return len(self.questionaris_importats)

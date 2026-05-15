from abc import ABC, abstractmethod


class Pregunta(ABC):
    def __init__(self, id_pregunta, id_questionari, enunciat, resposta_correcta, punts):
        self._id_pregunta = id_pregunta
        self._id_questionari = id_questionari
        self._enunciat = enunciat
        self._resposta_correcta = resposta_correcta
        self._punts = punts

    def get_id_pregunta(self): return self._id_pregunta
    def get_id_questionari(self): return self._id_questionari
    def get_enunciat(self): return self._enunciat
    def get_resposta_correcta(self): return self._resposta_correcta
    def get_punts(self): return self._punts

    @abstractmethod
    def get_tipus(self): pass

    @abstractmethod
    def get_respostes(self): pass

    @abstractmethod
    def validar_resposta(self, resposta): pass


class PreguntaVF(Pregunta):
    def __init__(self, id_pregunta, id_questionari, enunciat, resposta1, resposta2, resposta_correcta, punts):
        super().__init__(id_pregunta, id_questionari, enunciat, resposta_correcta, punts)
        self._resposta1 = resposta1
        self._resposta2 = resposta2

    def get_tipus(self): return "Verdader/Fals"

    def get_respostes(self): return [self._resposta1, self._resposta2]

    def validar_resposta(self, resposta):
        try:
            return int(resposta) == self._resposta_correcta
        except (ValueError, TypeError):
            return False


class PreguntaMultiple(Pregunta):
    def __init__(self, id_pregunta, id_questionari, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts):
        super().__init__(id_pregunta, id_questionari, enunciat, resposta_correcta, punts)
        self._resposta1 = resposta1
        self._resposta2 = resposta2
        self._resposta3 = resposta3
        self._resposta4 = resposta4

    def get_tipus(self): return "Múltiple"

    def get_respostes(self):
        return [r for r in [self._resposta1, self._resposta2, self._resposta3, self._resposta4] if r is not None]

    def validar_resposta(self, resposta):
        try:
            return int(resposta) == self._resposta_correcta
        except (ValueError, TypeError):
            return False

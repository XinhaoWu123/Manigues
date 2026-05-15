class Questionari:
    def __init__(self, id_questionari, id_propietari, titol, categoria, dificultat, descripcio, preguntes=None):
        self._id_questionari = id_questionari
        self._id_propietari = id_propietari
        self._titol = titol
        self._categoria = categoria
        self._dificultat = dificultat
        self._descripcio = descripcio
        self._preguntes = preguntes if preguntes is not None else []

    def get_id_questionari(self): return self._id_questionari
    def get_titol(self): return self._titol
    def get_categoria(self): return self._categoria
    def get_dificultat(self): return self._dificultat
    def get_descripcio(self): return self._descripcio
    def get_preguntes(self): return self._preguntes

    def add_pregunta(self, pregunta):
        self._preguntes.append(pregunta)

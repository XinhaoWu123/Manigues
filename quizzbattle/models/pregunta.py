from abc import ABC, abstractmethod
import random
class Pregunta(ABC):

    def __init__(self, id_pregunta, id_questionari, enunciat, resposta1, resposta2, resposta_correcta, punts, resposta3 = None, resposta4 = None):
        self.__id_pregunta = id_pregunta
        self.__id_questionari = id_questionari
        self.__enunciat = enunciat
        self.__resposta1 = resposta1
        self.__resposta2 = resposta2
        self.__resposta3 = resposta3
        self.__resposta4 = resposta4
        self.__resposta_correcta = resposta_correcta
        self.__punts = punts

    def get_id_pregunta(self):
        return self.__id_pregunta
    
    def set_id_pregunta(self, nou_id):
        self.__id_pregunta = nou_id

    def get_id_questionari(self):
        return self.__id_questionari
    
    def set_id_questionari(self, nou_id):
        self.__id_questionari = nou_id

    def get_enunciat(self):
        return self.__enunciat
    
    def set_enunciat(self, nou_enunciat):
        self.__enunciat = nou_enunciat

    def get_resposta1(self):
        return self.__resposta1
    
    def set_resposta1(self, nova_resposta):
        self.__resposta1 = nova_resposta

    def get_resposta2(self):
        return self.__resposta2
    
    def set_resposta2(self, nova_resposta):
        self.__resposta2 = nova_resposta

    def get_resposta3(self):
        return self.__resposta3
    
    def set_resposta3(self, nova_resposta):
        self.__resposta3 = nova_resposta

    def get_resposta4(self):
        return self.__resposta4
    
    def set_resposta4(self, nova_resposta):
        self.__resposta4 = nova_resposta

    def get_resposta_correcta(self):
        return self.__resposta_correcta
    
    def set_resposta_correcta(self, nova_resposta):
        self.__resposta_correcta = nova_resposta

    def get_punts(self):
        return self.__punts
    
    def set_punts(self, nous_punts):
        self.__punts = nous_punts

    @abstractmethod
    def validar(self, resposta_usuari: int) -> bool:
        pass

    def mostrar_pregunta(self):
        print(f"{self.__enunciat}")

    def __str__(self):
        return (f"ID Pregunta: {self.__id_pregunta}\n"
                f"ID Qüestionari: {self.__id_questionari}\n"
                f"Enunciat: {self.__enunciat}\n"
                f"Resposta 1: {self.__resposta1}\n"
                f"Resposta 2: {self.__resposta2}\n"
                f"Resposta 3: {self.__resposta3}\n"
                f"Resposta 4: {self.__resposta4}\n"
                f"Resposta correcta: {self.__resposta_correcta}\n"
                f"Punts: {self.__punts}")
    

class PreguntaVF(Pregunta):

    def __init__(self, id_pregunta, id_questionari,enunciat, resposta_correcta, punts):
        super().__init__(
            id_pregunta,
            id_questionari,
            enunciat,
            "Vertader",
            "Fals",
            resposta_correcta,
            punts
        )

    def validar(self, resposta_usuari) -> bool:
        return resposta_usuari == self.get_resposta_correcta()
    
    
class PreguntaMulti(Pregunta):
    def __init__(self, id_pregunta, id_questionari,enunciat, resposta_correcta, punts):
        super().__init__(
            id_pregunta,
            id_questionari,
            enunciat,
            "Vertader",
            "Fals",
            resposta_correcta,
            punts
        )

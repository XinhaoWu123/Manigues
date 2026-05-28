class Usuari:

    def __init__(self, nom, nom_usuari, contrassenya, email):
        self._nom = nom
        self._nom_usuari = nom_usuari
        self._contrassenya = contrassenya
        self._email = email

    def get_nom(self):
        return self._nom

    def set_nom(self, nou_nom):
        self._nom = nou_nom

    def get_nom_usuari(self):
        return self._nom_usuari

    def set_nom_usuari(self, nou_nom_usuari):
        self._nom_usuari = nou_nom_usuari

    def get_contrassenya(self):
        return self._contrassenya

    def set_contrassenya(self, nova_contrassenya):
        self._contrassenya = nova_contrassenya

    def get_email(self):
        return self._email

    def set_email(self, nou_email):
        self._email = nou_email

    def __str__(self):
        return (f"Nom: {self._nom}\n"
                f"Nom d'usuari: {self._nom_usuari}\n"
                f"Email: {self._email}")
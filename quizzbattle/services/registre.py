import mysql.connector
from database.database import get_connection
from models.usuari import Usuari


def registrar_usuari():
    """
    Demana les dades del nou usuari, crea un objecte Usuari,
    valida les dades i el guarda a la BD.
    """
    print("\n===== REGISTRE D'USUARI =====")

    nom = input("Nom complet: ").strip()
    nom_usuari = input("Nom d'usuari: ").strip()
    email = input("Email: ").strip()
    contrassenya = input("Contrasenya: ").strip()
    contrassenya2 = input("Repeteix la contrasenya: ").strip()

    # Validacions bàsiques
    if not nom or not nom_usuari or not email or not contrassenya:
        print("Tots els camps són obligatoris.")
        return False

    if contrassenya != contrassenya2:
        print("Les contrasenyes no coincideixen.")
        return False

    if "@" not in email or "." not in email:
        print(" El format de l'email no és vàlid.")
        return False

    # Creem l'objecte Usuari
    nou_usuari = Usuari(nom, nom_usuari, contrassenya, email)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO usuaris (nom, nom_usuari, contrassenya, email)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (
            nou_usuari.get_nom(),
            nou_usuari.get_nom_usuari(),
            nou_usuari.get_contrassenya(),
            nou_usuari.get_email()
        ))
        conn.commit()
        cursor.close()
        conn.close()

        print(f"\n Usuari '{nom_usuari}' registrat correctament!")
        return True

    except mysql.connector.IntegrityError as e:
        if "nom_usuari" in str(e):
            print("Aquest nom d'usuari ja existeix.")
        elif "email" in str(e):
            print("Aquest email ja està registrat.")
        else:
            print(f"Error d'integritat: {e}")
        return False

    except mysql.connector.Error as e:
        print(f"Error de base de dades: {e}")
        return False
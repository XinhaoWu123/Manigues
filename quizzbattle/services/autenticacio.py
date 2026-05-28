import mysql.connector
from database.database import get_connection


def iniciar_sessio():
    print("\n===== INICIAR SESSIÓ =====")

    nom_usuari = input("Nom d'usuari: ").strip()
    contrassenya = input("Contrasenya: ").strip()

    if not nom_usuari or not contrassenya:
        print(" El nom d'usuari i la contrasenya no poden estar buits.")
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT id_usuari, nom, nom_usuari, email,
            data_registre, num_partides, victories,
            derrotes, empats, puntuacio_total
            FROM usuaris
            WHERE nom_usuari = %s AND contrassenya = %s
        """
        cursor.execute(sql, (nom_usuari, contrassenya))
        usuari = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuari:
            print(f"\n✅ Benvingut/da, {usuari['nom']}!")
            return usuari
        else:
            print("Nom d'usuari o contrasenya incorrectes.")
            return None
    except mysql.connector.Error as e:
        print(f"Error de base de dades: {e}")
        return None
import mysql.connector

def calcular_puntuacio_final(punts_obtinguts, punts_totals):
    if punts_totals == 0:
        return 0.0
    return (punts_obtinguts / punts_totals) * 10

def guardar_partida(conn, id_questionari, tipus):
    cursor = conn.cursor()
    sql = "INSERT INTO partides (id_questionari, tipus) VALUES (%s, %s)"
    cursor.execute(sql, (id_questionari, tipus))
    conn.commit()
    return cursor.lastrowid

def guardar_resultat(conn, id_partida, id_usuari, puntuacio, resultat):
    cursor = conn.cursor()
    sql = """
        INSERT INTO resultats (id_partida, id_usuari, puntuacio, resultat)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (id_partida, id_usuari, puntuacio, resultat))
    conn.commit()

def finalitzar_questionari(conn, id_questionari, id_usuari, respostes_correctes, respostes_errades, punts_obtinguts, punts_totals):
    puntuacio_final = calcular_puntuacio_final(punts_obtinguts, punts_totals)

    if respostes_errades == 0:
        resultat = "WIN"
    else:
        resultat = "LOSE"

    id_partida = guardar_partida(conn, id_questionari, "INDIVIDUAL")
    guardar_resultat(conn, id_partida, id_usuari, round(puntuacio_final, 2), resultat)

    return {
        "encerts": respostes_correctes,
        "errades": respostes_errades,
        "puntuacio_final": round(puntuacio_final, 2)
    }
def guardar_partida_vs(conn, id_questionari, id_usuari1, id_usuari2, punts1, totals1, punts2, totals2):
    id_partida = guardar_partida(conn, id_questionari, "VS")

    puntuacio1 = calcular_puntuacio_final(punts1, totals1)
    puntuacio2 = calcular_puntuacio_final(punts2, totals2)

    if puntuacio1 > puntuacio2:
        r1, r2 = "WIN", "LOSE"
    elif puntuacio2 > puntuacio1:
        r1, r2 = "LOSE", "WIN"
    else:
        r1 = r2 = "DRAW"

    guardar_resultat(conn, id_partida, id_usuari1, round(puntuacio1, 2), r1)
    guardar_resultat(conn, id_partida, id_usuari2, round(puntuacio2, 2), r2)

    return {
        "puntuacio1": round(puntuacio1, 2),
        "puntuacio2": round(puntuacio2, 2),
        "resultat1": r1,
        "resultat2": r2
    }

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="quizbattle",
        auth_plugin='mysql_native_password'
    )
    
    return conn
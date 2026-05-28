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

def insert_questionari_db(conn, questionari_obj, id_propietari):
    cursor = conn.cursor()
    sql = "INSERT INTO questionaris (id_propietari, titol, categoria, dificultat, descripcio) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (id_propietari, questionari_obj.get_titol(), questionari_obj.get_categoria(), questionari_obj.get_dificultat(), questionari_obj.get_descripcio()))
    conn.commit()
    return cursor.lastrowid

def insert_pregunta_db(conn, pregunta_obj, id_questionari):
    cursor = conn.cursor()
    sql = "INSERT INTO preguntes (id_questionari, tipus, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (id_questionari, pregunta_obj.get_tipus(), pregunta_obj.get_enunciat(), pregunta_obj.get_resposta1(), pregunta_obj.get_resposta2(), pregunta_obj.get_resposta3(), pregunta_obj.get_resposta4(), pregunta_obj.get_resposta_correcta(), pregunta_obj.get_punts()))
    conn.commit()

def get_questionari_by_title_and_owner_db(conn, titol, id_propietari):
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT id_questionari, titol, categoria, dificultat, descripcio FROM questionaris WHERE titol = %s AND id_propietari = %s"
    cursor.execute(sql, (titol, id_propietari))
    questionari_data = cursor.fetchone()
    cursor.close()
    return questionari_data

def update_questionari_db(conn, questionari_obj, id_questionari):
    cursor = conn.cursor()
    sql = "UPDATE questionaris SET titol = %s, categoria = %s, dificultat = %s, descripcio = %s WHERE id_questionari = %s"
    cursor.execute(sql, (questionari_obj.get_titol(), questionari_obj.get_categoria(), questionari_obj.get_dificultat(), questionari_obj.get_descripcio(), id_questionari))
    conn.commit()

def delete_preguntes_by_questionari_id(conn, id_questionari):
    cursor = conn.cursor()
    sql = "DELETE FROM preguntes WHERE id_questionari = %s"
    cursor.execute(sql, (id_questionari,))
    conn.commit()
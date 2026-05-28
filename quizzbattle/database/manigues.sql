DROP DATABASE IF EXISTS quizbattle;
CREATE DATABASE quizbattle;

CREATE TABLE usuaris (
  id_usuari INT PRIMARY KEY AUTO_INCREMENT,
  nom VARCHAR(100) NOT NULL,
  nom_usuari VARCHAR(40) NOT NULL UNIQUE,
  contrassenya VARCHAR(255) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  data_registre DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  num_partides INT NOT NULL DEFAULT 0,
  victories INT NOT NULL DEFAULT 0,
  derrotes INT NOT NULL DEFAULT 0,
  empats INT NOT NULL DEFAULT 0,
  puntuacio_total DECIMAL(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE questionaris (
  id_questionari INT PRIMARY KEY AUTO_INCREMENT,
  id_propietari INT NOT NULL,
  titol VARCHAR(200) NOT NULL,
  categoria VARCHAR(100) NOT NULL,
  dificultat INT NOT NULL CHECK (dificultat BETWEEN 1 AND 5),
  descripcio TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_propietari) REFERENCES usuaris(id_usuari) ON DELETE CASCADE
);

CREATE TABLE preguntes (
  id_pregunta INT PRIMARY KEY AUTO_INCREMENT,
  id_questionari INT NOT NULL,
  tipus VARCHAR(50) NOT NULL,
  enunciat TEXT NOT NULL,
  resposta1 VARCHAR(500),
  resposta2 VARCHAR(500),
  resposta3 VARCHAR(500),
  resposta4 VARCHAR(500),
  resposta_correcta INT, -- 1..4
  punts INT NOT NULL DEFAULT 1, -- 1 o 2
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_questionari) REFERENCES questionaris(id_questionari) ON DELETE CASCADE,
  CHECK (resposta_correcta IS NULL OR (resposta_correcta BETWEEN 1 AND 4)),
  CHECK (
    resposta_correcta IS NULL
    OR (resposta_correcta = 1 AND resposta1 IS NOT NULL AND TRIM(resposta1) <> '')
    OR (resposta_correcta = 2 AND resposta2 IS NOT NULL AND TRIM(resposta2) <> '')
    OR (resposta_correcta = 3 AND resposta3 IS NOT NULL AND TRIM(resposta3) <> '')
    OR (resposta_correcta = 4 AND resposta4 IS NOT NULL AND TRIM(resposta4) <> '')
  )
);
DROP TABLE IF EXISTS partides;
CREATE TABLE partides (
  id_partida INT PRIMARY KEY AUTO_INCREMENT,
  id_questionari INT NOT NULL,
  tipus VARCHAR(10) NOT NULL, -- 'INDIVIDUAL' o 'VS'
  data_partida DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_questionari) REFERENCES questionaris(id_questionari) ON DELETE RESTRICT
) ENGINE=InnoDB;

DROP TABLE IF EXISTS resultats;
CREATE TABLE resultats (
  id_resultat INT PRIMARY KEY AUTO_INCREMENT,
  id_partida INT NOT NULL,
  id_usuari INT NOT NULL,
  puntuacio DECIMAL(5,2) NOT NULL, -- nota ponderada, per exemple 0.00 - 10.00
  resultat VARCHAR(10) NOT NULL, -- 'WIN', 'LOSE' o 'DRAW'
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_partida) REFERENCES partides(id_partida) ON DELETE CASCADE,
  FOREIGN KEY (id_usuari) REFERENCES usuaris(id_usuari) ON DELETE CASCADE,
  CHECK (puntuacio >= 0 AND puntuacio <= 10),
  CHECK (resultat IN ('WIN','LOSE','DRAW'))
)

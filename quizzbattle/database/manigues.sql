Drop database if exists quizbattle;
create database quizbattle;

create table usuaris (
id_usuari INT PRIMARY KEY auto_increment not null,
nom varchar(20) not null,
nom_usuari varchar(40) UNIQUE not null,
contrassenya varchar(40) not null,
email varchar(60) not null unique,
data_registre DATETIME not null,
num_partides INT not null default 0,
victories int not null default 0,
derrotes int not null default 0,
empats int not null default 0,
puntuacio_total float not null
);

create table questionaris (
id_questionari int primary key not null auto_increment,
id_propietari int not null,
titol varchar(40) not null,
categoria varchar(40) not null,





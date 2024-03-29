
DROP TABLE Utilisateur;
DROP TABLE Sessions;
DROP TABLE Token;
DROP TABLE Objectif;


create table Utilisateur (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom varchar(30) NOT NULL,
  email varchar(50) NOT NULL,
  salt varchar(32) NOT NULL,
  json text,
  hash varchar(128) NOT NULL
  -- situation TEXT CHECK( situation IN ('etudfull','etudpart','employe','autre') ) NOT NULL DEFAULT 'autre',
  
);
CREATE TABLE Objectif (
  id_utilisateur INTEGER NOT NULL,
  titre varchar(30) NOT NULL,
  duree REAL,
  frequence INTEGER,
  CHECK (frequence= 1 OR(frequence = 0))
);

create table Sessions (
  id_session varchar(500) primary key,
  email varchar(50) NOT NULL
);

create table Token (
  id integer NOT NULL primary key AUTOINCREMENT,
  email varchar(50) NOT NULL,
  exp varchar(50) NOT NULL, 
  token varchar(250) NOT NULL
);



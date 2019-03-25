
DROP TABLE Utilisateur;
DROP TABLE Sessions;
DROP TABLE Token;
DROP TABLE Evenement;
create table Evenement (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom_event varchar( 40 ) NOT NULL,
  recurrent integer,
  description text NOT NULL

);

create table Agenda (
  agendaid integer NOT NULL primary key AUTOINCREMENT
);

create table Utilisateur (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom varchar(30) NOT NULL,
  email varchar(50) NOT NULL,
  salt varchar(32) NOT NULL,
  agenda integer,
  hash varchar(128) NOT NULL
  foreign key (agenda) REFERENCES Agenda (agendaid)
  -- situation TEXT CHECK( situation IN ('etudfull','etudpart','employe','autre') ) NOT NULL DEFAULT 'autre',
  
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



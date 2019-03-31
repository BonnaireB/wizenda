
DROP TABLE Utilisateur;
DROP TABLE Sessions;
DROP TABLE Token;
DROP TABLE Evenement;

create table Evenement (
  id_agenda integer NOT NULL primary key,
  nom_event varchar( 20 ) NOT NULL,
  type_event varchar(15) NOT NULL,
  description text NOT NULL,
  couleur varchar(20),
  constraint fk_id
    FOREIGN KEY (id_agenda)
    REFERENCES  Agenda (id_utilisateur)
);

create table Agenda (
  id_utilisateur integer NOT NULL primary key,
  constraint fk_id
    FOREIGN KEY (id_utilisateur)
    REFERENCES Utilisateur (id)
)

create table Utilisateur (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom varchar(30) NOT NULL,
  email varchar(50) NOT NULL,
  salt varchar(32) NOT NULL,
  hash varchar(128) NOT NULL
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



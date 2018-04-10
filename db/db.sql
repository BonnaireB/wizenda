create table Animal (
  id integer NOT NULL primary key AUTOINCREMENT ,
  nom_animal varchar(20) NOT NULL,
  type_animal varchar(15) NOT NULL,
  race varchar(25) NOT NULL,
  age integer NOT NULL,
  description text NOT NULL,
  img LargeBinary
);

create table Utilisateur (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom varchar(25) NOT NULL,
  prenom varchar(30) NOT NULL,
  email varchar(50) NOT NULL,
  salt varchar(32) NOT NULL,
  hash varchar(128) NOT NULL,
  num_de_tel varchar(20) NOT NULL,
  adresse varchar(50) NOT NULL,
  ville varchar(50) NOT NULL,
  cp varchar(10) NOT NULL
);

create table Sessions (
  id integer primary key AUTOINCREMENT,
  id_session varchar(32) NOT NULL,
  email varchar(25) NOT NULL
);
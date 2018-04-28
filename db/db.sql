
DROP TABLE Animal;
DROP TABLE Utilisateur;
DROP TABLE Sessions;
DROP TABLE Token;
DROP TABLE Image;
create table Animal (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom_animal varchar( 20 ) NOT NULL,
  type_animal varchar(15) NOT NULL,
  race varchar(25) NOT NULL,
  age integer NOT NULL,
  description text NOT NULL,
  mail_proprio text NOT NULL,
  adresse text NOT NULL,
  image_id varchar(32)
);

create table Image (
  id varchar(32) primary key,
  image blob
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
  id_session varchar(500) primary key,
  email varchar(50) NOT NULL
);

create table Token (
  id integer NOT NULL primary key AUTOINCREMENT,
  email varchar(50) NOT NULL,
  exp varchar(50) NOT NULL, 
  token varchar(250) NOT NULL
);


insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio, adresse) values ("Bibi","Chat","Siamois",4,"petit mignon calin chaton beau male", "benjisosoph@gmail.com", "Montreal");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio, adresse) values ("Bobo","Chien","Errant",12,"gros violent sanguinaire", "benjisosoph@gmail.com", "Montreal");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio, adresse) values ("Vino","Chat","créole",11,"gros matou male chat sensible","benjisosoph@gmail.com", "Montreal");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio, adresse) values ("Link","Ecureuil","allemand",1,"petit mignon coquin beau male", "benjisosoph@gmail.com", "Montreal");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio, adresse) values ("Mario","Tortue","muette",119,"timide sanguinaire calin myope male", "benjisosoph@gmail.com", "Montreal");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio, adresse) values ("Sonic","Herisson","Piquant",44,"vieux Herisson Grincheux sublime male", "benjisosoph@gmail.com", "Montreal");

insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Sophie","Ph","benjisosoph@gmail.com","73ef09812fa2475cbd063b19cdc230da","3c1afccc289e53dd53922ef100d5b2e96d00036f876583e538653fd2b4bd25e00ce93dc49c926ff6121631cbc2198734bcd6853687170f6fdfb3237de79bf66c","0648244857","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Victor","benjisosoph@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Marcin","benjisosoph@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Mathieu","benjisosoph@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Suban","benjisosoph@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Nintendo","benjisosoph@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Sega","benjisosoph@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
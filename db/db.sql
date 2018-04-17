
create table Animal (
  id integer NOT NULL primary key AUTOINCREMENT,
  nom_animal varchar( 20 ) NOT NULL,
  type_animal varchar(15) NOT NULL,
  race varchar(25) NOT NULL,
  age integer NOT NULL,
  description text NOT NULL,
  mail_proprio text NOT NULL,
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
  prenom varchar(32) NOT NULL,
  email varchar(25) NOT NULL
);


insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio) values ("Bibi","Chat","Siamois",4,"petit mignon calin chaton beau male", "victorinf3005@gmail.com");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio) values ("Bobo","Chien","Errant",12,"gros violent sanguinaire", "marcinf3005@gmail.com");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio) values ("Vino","Chat","créole",11,"gros matou male chat sensible","mathieuinf3005@gmail.com");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio) values ("Link","Ecureuil","allemand",1,"petit mignon coquin beau male", "subaninf3005@gmail.com");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio) values ("Mario","Tortue","muette",119,"timide sanguinaire calin myope male", "nintendoinf3005@gmail.com");
insert into Animal (nom_animal,type_animal,race,age,description,mail_proprio) values ("Sonic","Herisson","Piquant",44,"vieux Herisson Grincheux sublime male", "segainf3005@gmail.com");

insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Victor","victorinf3005@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Marcin","marcinf3005@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Mathieu","mathieuinf3005@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Suban","subaninf3005@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Nintendo","nintendoinf3005@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
insert into Utilisateur (nom,prenom,email,salt,hash,num_de_tel,adresse,ville,cp) values ("Marcelin","Sega","segainf3005@gmail.com","x3411234sbhbd","s3443b3451n2342b121","514-555 5555","2789 Rue Gamelin", "Montreal", "H4C 3X2");
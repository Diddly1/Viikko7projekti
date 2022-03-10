-- CREATE DATABASE tyotunnit;
-- SELECT NOW();

CREATE TABLE tyo_taulu (
    id              SERIAL PRIMARY KEY,
    nimi            varchar(255) NOT NULL,
    alku            TIMESTAMP NOT NULL,
    loppu           TIMESTAMP NOT NULL,
    projekti_nimi   varchar(255) NOT NULL,
    selite          varchar NOT NULL,
    lampotila       DECIMAL(5,2)
 );

 INSERT INTO tyo_taulu
     (nimi,alku,loppu,projekti_nimi,selite) 
     VALUES ('matti',TIMESTAMP '2011-05-16 15:36:38',TIMESTAMP '2011-05-16 15:36:38','blabla','blablabla');

SELECT * FROM tyo_taulu;
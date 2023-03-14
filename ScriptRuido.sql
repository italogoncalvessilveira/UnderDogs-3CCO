create database ruido;
use ruido; 

create table nivel_ruido(
id integer auto_increment primary key,
decibel decimal(4,2),
ambiente boolean,
espaco double,
duracao  double); 

select * from nivel_ruido;
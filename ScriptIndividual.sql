create database movimento;
use movimento;

create table sensor_movimento(
id_leitura integer auto_increment primary key,
aceleracao_eixo_x varchar(10),
aceleracao_eixo_y varchar(10),
aceleracao_eixo_z varchar(10),
horario_leitura time,
memoria double,
duracao_execucao double
);

select * from sensor_movimento;
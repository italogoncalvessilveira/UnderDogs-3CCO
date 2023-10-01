import pandas as pd
import mysql.connector

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius
    

def criar_conexao():
    cnx = mysql.connector.connect(user='admin',
                                  password='urubu100',
                                  host='rds-underdogs.cfzmhji6igm5.us-east-1.rds.amazonaws.com',
                                  database='Grupo3')
    return cnx


def insert_query(data, query):
    cnx = criar_conexao()
    cursor = cnx.cursor()

    cursor.executemany(query, data)

    cnx.commit()
    cursor.close()
    cnx.close()
    return

query_address = 'INSERT INTO clima(temperatura_media, regiao,mes) values(%s, %s, %s)'

listaClima = []


input_csv = r'C://Users/italo/Desktop/f91c3ca6-7c9f-7d1e-f004-4ea88b7d73ab.csv'


df = pd.read_csv(input_csv)


def extract_fields(row):
    listaClima.append((fahrenheit_to_celsius(row[1]), row[3], row[8]))


df.apply(extract_fields, axis=1)


insert_query(listaClima, query_address)


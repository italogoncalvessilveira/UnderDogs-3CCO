import mysql.connector
from mysql.connector import errorcode
import json

def load_credentials():
    with open('secrets.json') as secrets:
        cred = json.load(secrets)
        return cred
    
def connection():
    credentials = load_credentials()
    try:
        conn = mysql.connector.connect(
            host=credentials['host'], 
            user=credentials['user'], 
            password=credentials['password'], 
            database=credentials['database'],
            port=credentials['port'])
        print("Conectado ao banco de dados")
        return conn
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or password is wrong")
        else:
            print(error)

def insert(conn,leitura,time):
    cursor = conn.cursor()

    query = f"INSERT INTO SENSOR_TEMPERATURA (TEMPERATURA, DATA_LEITURA) VALUES ('{leitura}', '{time}');"
    cursor.execute(query)

    cursor.close()

def insert_log(conn,tempo,espaco,maquina):
    cursor = conn.cursor()

    query = f"INSERT INTO LOG (TEMPO, ESPACO, MAQUINA) VALUES ('{tempo}', '{espaco}', '{maquina}');"
    cursor.execute(query)

    cursor.close()
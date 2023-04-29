import mysql.connector
from mysql.connector import errorcode
import json
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plot

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

def web():
    conn = connection()
    local = pd.read_sql(f"SELECT tempo AS TEMPO_LOCAL, espaco AS ESPACO_LOCAL FROM LOG WHERE maquina = 'LOCAL'",conn)
    local.columns = local.columns.str.upper()

    cloud = pd.read_sql(f"SELECT tempo AS TEMPO_AWS, espaco AS ESPACO_AWS FROM LOG WHERE maquina = 'AWS'",conn)
    cloud.columns = cloud.columns.str.upper()

    temp = pd.read_sql(f"""WITH cte AS (
                    SELECT MAX(id_temp)/2 FROM sensor_temperatura  
                    )
                    SELECT
                        temperatura,
                        data_leitura
                    FROM
                        sensor_temperatura
                    WHERE
                        id_temp<(SELECT*FROM cte)
                    GROUP BY
                        temperatura,
                        data_leitura""",conn)
    temp.columns = temp.columns.str.upper()
    conn.close()


    teste = pd.DataFrame()
    teste['TEMPO_LOCAL'] = local['TEMPO_LOCAL']
    teste['ESPACO_LOCAL'] = local['ESPACO_LOCAL']
    teste['TEMPO_AWS'] = cloud['TEMPO_AWS']
    teste['ESPACO_AWS'] = cloud['ESPACO_AWS']

    teste = teste.astype(float)
    temp = temp.astype({"TEMPERATURA": float})

    st.subheader('Comparação TEMPO LOCAL x TEMPO AWS')
    st.line_chart(data=teste, y=['TEMPO_AWS', 'TEMPO_LOCAL'])

    st.subheader('Comparação ESPACO LOCAL x ESPACO AWS')
    st.line_chart(teste, y=['ESPACO_AWS', 'ESPACO_LOCAL'])

    st.subheader('Variação da Temperatura durante a noite de sono')
    st.line_chart(temp, x='DATA_LEITURA', y='TEMPERATURA')

# "background": "#0e1117"

    # plot.title("ESPACO X TEMPO")
    # plot.plot()
    # plot.xlabel("Tempo")
    # plot.ylabel("Hora")
    # st.pyplot(plot.show())

if __name__ == '__main__':
    web()
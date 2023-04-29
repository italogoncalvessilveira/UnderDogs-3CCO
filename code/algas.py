# from matplotlib import pyplot as plot
import time
import sys
from insert_db import insert,connection


def algas(leituras,times):

    listaEspaco = []
    listaTempo = []

    conn = connection()
    for i in range(0,len(leituras)):
        inicioProcessamentoA = time.time()
        insert(conn,leituras[i], times[i])


        fimProcessamentoA = time.time()
        duracaoA = fimProcessamentoA - inicioProcessamentoA

        espacoA = (sys.getsizeof(str(leituras[i])+times[i]) / (1024))
            


        listaEspaco.append(round(espacoA,6))
        listaTempo.append(round(duracaoA,6))


    conn.commit() 
    conn.close()


    return [listaTempo, listaEspaco]
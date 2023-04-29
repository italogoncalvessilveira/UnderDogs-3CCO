
from algas import algas
import random
import datetime
from matplotlib import pyplot as plot
from insert_db import insert_log,connection



def run():
    leituras = []
    times = []

    leituras_hora = []

    times_graph = []
    
    temp_inicial = random.randint(-10, 40)
    time_inicial = datetime.datetime.now()

    mins = 0

    h = int(input('Digite a qtd de horas de sono para a simulação: '))
    qtd_horas = list(range(10,70,10))
    for x in range(0,h*6):
        temp_inicial = temp_inicial+random.uniform(0, 1)
        temp_inicial = temp_inicial-random.uniform(0, 1)
        for i in range(0,10):
            delta=datetime.timedelta(minutes=i+mins)
            time_final = time_inicial+delta
            temp = random.uniform(temp_inicial, temp_inicial+random.uniform(0, 1))
            temp = random.uniform(temp-random.uniform(0, 1),temp)
            leituras.append(round(temp,2))
            times.append(time_final.strftime('%Y-%m-%d %H:%M:%S'))
            times_graph.append(time_final.strftime('%H%M%S'))
            if i == 9:
                temp_inicial = round(temp,2)
        if mins%60 == 0:
            leituras_hora.append(leituras[-6:])
        mins = mins+10

    retorno_algas = algas(leituras, times)
    listaTempo=retorno_algas[0]
    listaEspaco=retorno_algas[1]

    conn = connection()
    for i in range(len(listaEspaco)):
        insert_log(conn,listaTempo[i], listaEspaco[i], 'AWS')
    
    conn.commit() 
    conn.close()



    # plot.title("Temperatura X Hora")
    # plot.plot(times_graph,leituras)
    # plot.xlabel("Tempo")
    # plot.ylabel("Hora")
    # plot.show()

    # for i in range(0,len(leituras_hora)):
    #     plot.plot(qtd_horas,leituras_hora[i],label=f'{i+1} hora de sono')

    # plot.title("Temperatura X Minutos de cada hora de sono")
    # plot.legend(loc='upper left')
    # plot.xlabel("Minutos")
    # plot.ylabel("Temperatura")
    # plot.show()


    # plot.title("Tempo e Espaço")
    # plot.xlabel("Tempo")
    # plot.ylabel("Espaco")
    # plot.plot(listaTempo)
    # plot.plot(listaEspaco)
    # plot.show()

    # plot.title("Tempo")
    # plot.plot(listaTempo)
    # plot.show()

    # plot.title("Espaço")
    # plot.plot(listaEspaco)
    # plot.show()

    # print(leituras)
    # print(times)
    # print(listaTempo)
    # print(listaEspaco)
    # print(leituras_hora)


if __name__ == '__main__':
    run()
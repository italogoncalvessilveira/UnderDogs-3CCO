import mysql.connector
import time
import random
from matplotlib import pyplot as plot
from sys import getsizeof


def insert_db(nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado):
    try:  
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Renato2002",
            database = "frequenciacardiaca"
        )

        if mydb.is_connected():
            db_Info = mydb.get_server_info()
            print("Conectado ao MySQL Server versão ", db_Info)

            mycursor = mydb.cursor()

            sql_query = "INSERT INTO FrequenciaCardiacaXPerfomance(nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = [nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado]
            mycursor.execute(sql_query, val)

            mydb.commit()

            print(mycursor.rowcount, f"registro inserido sobre o Paciente {nomePaciente}")
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("Conexão com MySQL está fechada\n")


try:
    
    vetNomePaciente = ["Marise","Alex","Italo","Maria", "Roberto"]
    vetIdadePaciente = ["48","40","20","65","80"]
    vetGeneroPaciente = ["F","M","M","F","M"]
    vetEspacoUtilizado = []
    vetTempoUtilizado = []

    FrequenciaCardiaca48Anos = []
    FrequenciaCardiaca40Anos = []
    FrequenciaCardiaca20Anos = []
    FrequenciaCardiaca65Anos = []
    FrequenciaCardiaca80Anos = []

    pacienteId = 0

    
    
    while True:
        pacienteId += 1

        if (pacienteId == 1):
            dataLeitura = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            if (len(FrequenciaCardiaca48Anos) == 0):
                FrequenciaCardiaca48Anos.append(random.randrange(57, 120))

            else:
                regraRandomica = random.randrange(0,2)
                if(regraRandomica == 0):
                    FrequenciaCardiaca48Anos.append(random.randrange(FrequenciaCardiaca48Anos[-1], FrequenciaCardiaca48Anos[-1] + 3))
                elif(regraRandomica == 1):
                    FrequenciaCardiaca48Anos.append(random.randrange(FrequenciaCardiaca48Anos[-1] - 2,FrequenciaCardiaca48Anos[-1]))
            
            time.sleep(1)
            plot.xlabel("Numero da Medição")
            plot.ylabel("Frequencia Cardiaca Paciente")
            plot.title("Paciente Marise Frequencia Cardiaca")
            plot.plot(FrequenciaCardiaca48Anos)
            
            insert_db(vetNomePaciente[0], vetIdadePaciente[0], vetGeneroPaciente[0], FrequenciaCardiaca48Anos[-1],dataLeitura, "20", "20")
        
        elif (pacienteId == 2):    
            dataLeitura = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            if (len(FrequenciaCardiaca40Anos) == 0):
                FrequenciaCardiaca40Anos.append(random.randrange(57, 120))

            else:
                regraRandomica = random.randrange(0,2)
                if(regraRandomica == 0):
                    FrequenciaCardiaca40Anos.append(random.randrange(FrequenciaCardiaca40Anos[-1], FrequenciaCardiaca40Anos[-1] + 3))
                elif(regraRandomica == 1):
                    FrequenciaCardiaca40Anos.append(random.randrange(FrequenciaCardiaca40Anos[-1] - 2,FrequenciaCardiaca40Anos[-1]))
            
            time.sleep(1)
            insert_db(vetNomePaciente[1], vetIdadePaciente[1], vetGeneroPaciente[1], FrequenciaCardiaca40Anos[-1],dataLeitura, "20", "20")
        
        elif (pacienteId == 3):    
            dataLeitura = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            if (len(FrequenciaCardiaca20Anos) == 0):
                FrequenciaCardiaca20Anos.append(random.randrange(57, 120))

            else:
                regraRandomica = random.randrange(0,2)
                if(regraRandomica == 0):
                    FrequenciaCardiaca20Anos.append(random.randrange(FrequenciaCardiaca20Anos[-1], FrequenciaCardiaca20Anos[-1] + 3))
                elif(regraRandomica == 1):
                    FrequenciaCardiaca20Anos.append(random.randrange( FrequenciaCardiaca20Anos[-1] - 2,FrequenciaCardiaca20Anos[-1]))
            
            time.sleep(1)
            insert_db(vetNomePaciente[2], vetIdadePaciente[2], vetGeneroPaciente[2], FrequenciaCardiaca20Anos[-1],dataLeitura, "20", "20")

        elif (pacienteId == 4):    
            dataLeitura = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            if (len(FrequenciaCardiaca65Anos) == 0):
                FrequenciaCardiaca65Anos.append(random.randrange(57, 120))

            else:
                regraRandomica = random.randrange(0,2)
                if(regraRandomica == 0):
                    FrequenciaCardiaca65Anos.append(random.randrange(FrequenciaCardiaca65Anos[-1], FrequenciaCardiaca65Anos[-1] + 3))
                elif(regraRandomica == 1):
                    FrequenciaCardiaca65Anos.append(random.randrange( FrequenciaCardiaca65Anos[-1] - 2,FrequenciaCardiaca65Anos[-1]))
            time.sleep(1)
            insert_db(vetNomePaciente[3], vetIdadePaciente[3], vetGeneroPaciente[3], FrequenciaCardiaca65Anos[-1],dataLeitura, "20", "20")
        
        elif (pacienteId == 5):    
            dataLeitura = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            if (len(FrequenciaCardiaca80Anos) == 0):
                FrequenciaCardiaca80Anos.append(random.randrange(57, 120))

            else:
                regraRandomica = random.randrange(0,2)
                if(regraRandomica == 0):
                    FrequenciaCardiaca80Anos.append(random.randrange(FrequenciaCardiaca80Anos[-1], FrequenciaCardiaca80Anos[-1] + 3))
                elif(regraRandomica == 1):
                    FrequenciaCardiaca80Anos.append(random.randrange(FrequenciaCardiaca80Anos[-1] - 2,FrequenciaCardiaca80Anos[-1]))
            
            time.sleep(1)
            insert_db(vetNomePaciente[4], vetIdadePaciente[4], vetGeneroPaciente[4], FrequenciaCardiaca80Anos[-1], dataLeitura, "20", "20")

            pacienteId = 0

        
except KeyboardInterrupt:
    pass
import mysql.connector
import time
import random
from matplotlib import pyplot as plot
import sys
from azure.iot.device import IoTHubDeviceClient, Message
import json

conn_str = "HostName=IoTHubDefinitivo.azure-devices.net;DeviceId=dispositivo-integracao-azureAws;SharedAccessKey=gOp+MTWrr0jsJrVIJ+mz1XQoS84e83TsAll2TPGa15o="
client = IoTHubDeviceClient.create_from_connection_string(conn_str)

bateriaDisponivel = 100


class Paciente:
    def __init__(self, nome, idade, genero):
        self.nome = nome
        self.idade = idade
        self.genero = genero


def plotagem():
            fig, axs = plot.subplots(2, 1, constrained_layout=True)
            axs[0].plot(FrequenciaCardiacaPaciente)
            axs[0].set_title('Frequencia Cardiaca Marise')
            axs[0].set_xlabel('Numero da Medição')
            axs[0].set_ylabel('Frequencia Cardiaca Paciente')
            
            axs[1].plot(vetEspacoUtilizado, '--',label='Espaço')
            axs[1].plot(vetTempoUtilizado, 'x-', label='Tempo')
            axs[1].set_title('Dados da Maquina')
            axs[1].set_xlabel('Numero da Medição')
            axs[1].set_ylabel('Espaço & Tempo') 
            axs[1].legend()

 
def regraRandomica():
            varRandomica = random.randrange(0,2)
            if(varRandomica == 0):
                    FrequenciaCardiacaPaciente.append(random.randrange(FrequenciaCardiacaPaciente[-1], FrequenciaCardiacaPaciente[-1] + 3))
            elif(varRandomica == 1):
                    FrequenciaCardiacaPaciente.append(random.randrange(FrequenciaCardiacaPaciente[-1] - 2,FrequenciaCardiacaPaciente[-1]))
                    

def decrementa_bateria():
    global bateriaDisponivel
    bateriaDisponivel -= 0.01


def insert_iotHub(nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado,zonaDisponibilidade,bateriaDisponivel):
        
        bateriaDisponivelFormat = "{:.2f}".format(bateriaDisponivel)   
           
        dados = {'nomePaciente': nomePaciente, 'idadePaciente': idadePaciente, 'generoPaciente': generoPaciente, 'frequenciaCardiaca': frequenciaCardiaca, 'dataLeitura': dataLeitura,'espacoUtilizado': espacoUtilizado,'tempoUtilizado': tempoUtilizado, 'zonaDisponibilidade': zonaDisponibilidade, 'bateriaDisponivel': bateriaDisponivelFormat}
        
        mensagem_json = json.dumps(dados)
        msg = Message(mensagem_json)

        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"

        client.send_message(msg)
        tamanhoMensagem = (len(str(msg))) / 1024 
        client.disconnect()
            
        print(dados)
        print(f"Tamanho da Mensagem em KB = {tamanhoMensagem}")
        decrementa_bateria()
        


def insert_db(nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado,zonaDisponibilidade):
    try:  
        mydb = mysql.connector.connect(
            # host="frequenciacardiaca.mysql.database.azure.com",
            # user="roott",
            # password="Urubu100",
            # database = "frequenciacardiaca"
            user= "roott",
            password= "Urubu100",
            host= "frequenciacardiaca.mysql.database.azure.com",
            database= "Grupo3"
        )

        if mydb.is_connected():
            #db_Info = mydb.get_server_info()
            #print("Conectado ao MySQL Server versão ", db_Info)

            mycursor = mydb.cursor()

            sql_query = "INSERT INTO FrequenciaCardiacaXPerfomance(nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado,zonaDisponibilidade) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = [nomePaciente,idadePaciente,generoPaciente,frequenciaCardiaca,dataLeitura,espacoUtilizado,tempoUtilizado,zonaDisponibilidade]
            mycursor.execute(sql_query, val)
            
            mydb.commit()

            print(mycursor.rowcount, f"registro inserido sobre o Paciente {nomePaciente} na AZ {zonaDisponibilidade}")           
            
            
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("Conexão com MySQL está fechada\n")


try:
    Paciente1 = Paciente("Italo", 20, "M")
        
    vetEspacoUtilizado = []
    vetTempoUtilizado = []

    FrequenciaCardiacaPaciente = []

    
    while True:
            
            inicio_processamento = time.time()
            dataLeitura = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            if (len(FrequenciaCardiacaPaciente) == 0):
                FrequenciaCardiacaPaciente.append(random.randrange(57, 120))
 
            else:
                regraRandomica()
            
            fim_processamento = time.time()
            duracao = fim_processamento - inicio_processamento
            espaco = sys.getsizeof(FrequenciaCardiacaPaciente) / (1024 * 1024)

            vetEspacoUtilizado.append(espaco)
            vetTempoUtilizado.append(duracao)

            tamanhodaLista = len(vetTempoUtilizado)
          
            #insert_db(Paciente1.nome, Paciente1.idade, Paciente1.genero, FrequenciaCardiacaPaciente[-1],dataLeitura, espaco, duracao, "localhost")
            insert_iotHub(Paciente1.nome, Paciente1.idade, Paciente1.genero, FrequenciaCardiacaPaciente[-1],dataLeitura, espaco, duracao, "localhost",bateriaDisponivel)
            
            #if len(FrequenciaCardiacaPaciente) % 10 == 0:
            #   plotagem()
                  
except KeyboardInterrupt:
    pass
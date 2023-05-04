import asyncio
import os
import random
import datetime
from azure.iot.device import IoTHubSession, MQTTError, MQTTConnectionFailedError

CONNECTION_STRING = "HostName=Gabriel02211021.azure-devices.net;DeviceId=Gabriel02211021;SharedAccessKey=M1n1KsMxr5R04OQqGIhXslDZpKBYEDpamOkZ+Z8iaTc="
TOTAL_MESSAGES_SENT = 0
total_messages_failed = 0

async def main():
    global TOTAL_MESSAGES_SENT
    print("Starting telemetry sample")
    print("Press Ctrl-C to exit")
    try:
        global TOTAL_MESSAGES_SENT
        print("Connecting to IoT Hub...")
        async with IoTHubSession.from_connection_string(CONNECTION_STRING) as session:
            print("Connected to IoT Hub")
            h = int(input('Digite a qtd de horas de sono para a simulação: '))
            if (random.randint(0, 100) < 3):
                    total_messages_failed += 1
                    print("Failure sending message. Messages failed: {}".format(total_messages_failed))
            else:
                temp_inicial = random.randint(-10, 40)
                time_inicial = datetime.datetime.now()
                mins = 0
                bateria = 100
                for x in range(0,h*6):
                    temp_inicial = temp_inicial+random.uniform(0, 1)
                    temp_inicial = temp_inicial-random.uniform(0, 1)
                    for i in range(0,10):
                        bateria = bateria-((0.01/100)*bateria)
                        delta=datetime.timedelta(minutes=i+mins)
                        time_final = time_inicial+delta
                        temp = random.uniform(temp_inicial, temp_inicial+random.uniform(0, 1))
                        temp = random.uniform(temp-random.uniform(0, 1),temp)
                        TOTAL_MESSAGES_SENT += 1

                        json_mensagem={
                            "messageId": TOTAL_MESSAGES_SENT,
                            "deviceId": 'Gabriel02211021',
                            "temperature": round(temp,2),
                            "horarioLeitura": time_final.strftime('%Y-%m-%d %H:%M:%S'),
                            "bateria": f"{round(bateria,2)}%"
                        }

                        print("Sending Message #{}...".format(json_mensagem))
                        await session.send_message("{}".format(json_mensagem))
                        print("Send Complete")


                        if i == 9:
                            temp_inicial = round(temp,2)

                        await asyncio.sleep(10)
                    mins = mins+10

    except MQTTError:
        # Connection has been lost.
        print("Dropped connection. Exiting")
    except MQTTConnectionFailedError:
        # Connection failed to be established.
        print("Could not connect. Exiting")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Exit application because user indicated they wish to exit.
        # This will have cancelled `main()` implicitly.
        print("User initiated exit. Exiting")
    finally:
        print("Sent {} messages in total".format(TOTAL_MESSAGES_SENT))
        print("{} messages failed in total".format(total_messages_failed))

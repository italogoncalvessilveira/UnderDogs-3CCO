import tweepy
import mysql.connector

def insert_db():
    try:  
        mydb = mysql.connector.connect(
            user= "roott",
            password= "Urubu100",
            host= "frequenciacardiaca.mysql.database.azure.com",
            database= "Grupo3"
        )

        if mydb.is_connected():
            #db_Info = mydb.get_server_info()
            #print("Conectado ao MySQL Server versão ", db_Info)

            mycursor = mydb.cursor()

            sql_query = "INSERT INTO analise_twitter(fraseTweet,sentimentoTweet,origem) VALUES (%s,%s,%s)"
            val = [lista_tweets[i],sentimento,"Italo"]
            mycursor.execute(sql_query, val)
            
            mydb.commit()

            print(mycursor.rowcount, "registro inserido")           
            
            
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            #print("Conexão com MySQL está fechada\n")


lista_tweets = []

def busca_twitter(fraseProcurada,qtdTweets):
# Chaves de API do Twitter
    consumer_key = "8CNb9XmJ7KrjOLp8UMNH9Fznh"
    consumer_secret = "eGoW01Xjhg1rslbOk23UYIPBsItB6Qr0cOA4SDmiXGekWfPmDB"
    access_token = "2973742181-XBE1qdfNncM8zrb5shvdKHLcJa1fvhvahPKQGjX"
    access_token_secret = "qRGj0HK2MIKWZHlIuiZ2oConS7yNPIRQwrqgoP0sAyI10"

# Autenticação com a API do Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

# Consulta de tweets
    
    tweets = api.search_tweets(q=fraseProcurada, tweet_mode="extended", count=qtdTweets)

# print(tweets)

    for tweet in tweets:
        if hasattr(tweet, "retweeted_status"):
            cleaned_text = tweet.retweeted_status.full_text
        else:
            cleaned_text = tweet.full_text
    
        lista_tweets.append(cleaned_text)

    


def analisar_sentimento(frase):
    # Lista de palavras-chave para sentimento positivo e negativo
    palavras_positivas = ["bom", "ótimo", "incrível", "feliz","Abraço", "Acolhedor", "Agradável", "Ânimo", "Amabilidade", "Amigo", "Amor", "Animação", "Apaixonado", "Aplauso", "Apreciar", "Aprovação", "Ardente", "Arrebatador", "Arrebatamento", "Artístico", "Astuto", "Atencioso", "Atraente", "Autoconfiante", "Autêntico", "Aventura", "Aventuroso", "Avivar", "Batalhador", "Beleza", "Benéfico", "Bondade", "Brilhante", "Brisa", "Caloroso", "Camaradagem", "Carinho", "Celebração", "Céu", "Charme", "Cintilar", "Coletivo", "Colorido", "Comemoração", "Compaixão", "Compreensão", "Conexão", "Confete", "Confiança", "Conforto", "Conquista", "Consciente", "Contentamento", "Coração", "Coragem", "Cordialidade", "Criatividade", "Cuidado", "Cumplicidade", "Curiosidade", "Dançar", "Deleite", "Delicadeza", "Desabrochar", "Desafio", "Descontraído", "Descoberta", "Desfrutar", "Desejo", "Destacar", "Dignidade", "Divertido", "Doçura", "Dourado", "Épico", "Êxtase", "Elegância", "Elevado", "Emoção", "Encantador", "Encorajar", "Energia", "Entusiasmo", "Especial", "Esperança", "Espetacular", "Espirituoso", "Estimular", "Estonteante", "Estrela", "Êxito", "Êxtase", "Explorar", "Expressar", "Fascinante", "Feliz", "Felicidade", "Festejar", "Firmeza", "Florescer", "Fluir", "Fortuna", "Frase", "Frescor", "Futuro", "Ganhar", "Generosidade", "Gentileza", "Glorioso", "Gratidão", "Grato", "Harmonia", "Heroico", "Honrar", "Iluminar", "Imaginação", "Impressionante", "Incentivar", "Incrível", "Inesquecível", "Inovador", "Insight", "Inspirador", "Integrar", "Intenso", "Intuição", "Júbilo", "Liberdade", "Líder", "Luz", "Magia", "Majestoso", "Maravilha", "Melodia", "Memorável", "Mente aberta", "Milagre", "Motivação", "Nascer", "Natureza", "Nobreza", "Oportunidade", "Orgulho", "Otimismo", "Paixão", "Parceria", "Paz", "Perdão", "Perseverança", "Prazer", "Precioso", "Preparado",]
    palavras_negativas = ["ruim", "terrível", "triste", "frustrado","desfavorável", "crime", "negativo", "destrutivo", "funesto", "degradante", "deplorável", "desabonador", "adverso", "inconveniente", "hostil", "desedificante","Abandono", "Abatido", "Abuso", "Acidente", "Acusação", "Adversidade", "Aflição", "Agonia", "Alarmante", "Amargura", "Amarras", "Ambivalente", "Angústia", "Aniquilar", "Ansiedade", "Apatia", "Apreensivo", "Arrependimento", "Assustador", "Atormentado", "Ausência", "Avaria", "Avareza", "Azar", "Bancarrota", "Barricada", "Beligerante", "Bilioso", "Blasfêmia", "Boicote", "Calamidade", "Caos", "Cegueira", "Censura", "Ceticismo", "Chantagem", "Chocante", "Choramingar", "Cobiça", "Colapso", "Colisão", "Combate", "Complacência", "Conflito", "Confusão", "Consequências", "Constrangimento", "Contaminação", "Contradição", "Controvérsia", "Corrupção", "Covardia", "Crise", "Crueldade", "Culpa", "Culpado", "Decepção", "Degradação", "Delinquência", "Delírio", "Demolição", "Depressão", "Desacordo", "Desafiador", "Desamparo", "Desânimo", "Desastre", "Descarrilamento", "Descaso", "Descontentamento", "Descontrole", "Descrença", "Descuido", "Desemprego", "Desesperança", "Desespero", "Desgosto", "Desilusão", "Deslealdade", "Desmantelamento", "Desmotivação", "Desolação", "Desordem", "Desperdício", "Desprezo", "Destroço", "Destruição", "Deturpação", "Devastação", "Dificuldade", "Dilema", "Discórdia", "Discriminação", "Disputa", "Distorção", "Divisão", "Doença", "Doloroso", "Dor", "Dúvida", "Egoísmo", "Embate", "Embuste", "Embaraçoso", "Emergência", "Encrenca", "Engano", "Envenenamento", "Escuridão", "Escândalo", "Escassez", "Esfacelamento", "Esquecimento", "Esvaziamento", "Evasivo", "Exclusão", "Extermínio", "Extravio", "Falência", "Falsidade", "Fatalidade", "Fiasco", "Fobia", "Fraqueza"]
    
    
    frase = frase.lower().replace(",", "").replace(".", "")
    
    palavras = frase.split()
    
    # Verificar se a frase contém palavras positivas ou negativas
    tem_sentimento_positivo = any(palavra in palavras for palavra in palavras_positivas)
    tem_sentimento_negativo = any(palavra in palavras for palavra in palavras_negativas)
    
    # Determinar o sentimento com base nas palavras encontradas
    if tem_sentimento_positivo and not tem_sentimento_negativo:
        sentimento = "positivo"
    elif tem_sentimento_negativo and not tem_sentimento_positivo:
        sentimento = "negativo"
    else:
        sentimento = "neutro"
    
    return sentimento


# Execução

busca_twitter("Racismo",5)

for i, frase in enumerate(lista_tweets):
    sentimento = analisar_sentimento(lista_tweets[i])
    print(lista_tweets[i])
    print("Sentimento da frase:", sentimento + "\n")
    insert_db()



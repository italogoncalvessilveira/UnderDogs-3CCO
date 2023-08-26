#iniciar spark
from pyspark import SparkConf
from pyspark.sql import SparkSession
import json
import boto3

conf = SparkConf()
conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'com.amazonaws.auth.InstanceProfileCredentialsProvider')
spark = SparkSession.builder.config(conf=conf).getOrCreate()


bucket_trusted = 'trusted-dev-italo'
bucket_refined = 'refined-dev-italo'



caminho_arquivo_s3 = 's3a://raw-dev-italo/88a4be99-901e-00a1-3abd-91907a0616a8.json'
file_name = '88a4be99-901e-00a1-3abd-91907a0616a8.json'


df = spark.read.json(caminho_arquivo_s3)    

df.show()


new_df_trusted = df.select(df.Body.nomePaciente.alias('nome_paciente'),
                           df.Body.idadePaciente.alias('idadePaciente'),
                           df.Body.generoPaciente.alias('generoPaciente'),
                           df.Body.frequenciaCardiaca.alias('frequenciaCardiaca'),
                           df.Body.dataLeitura.alias('dataLeitura'),
                           df.Body.espacoUtilizado.alias('espacoUtilizado'),
                           df.Body.tempoUtilizado.alias('tempoUtilizado'),
                           df.Body.zonaDisponibilidade.alias('zonaDisponibilidade'),
                           df.Body.bateriaDisponivel.alias('bateriaDisponivel'))


new_df_trusted.show()

dados_trusted = new_df_trusted.collect()


json_trusted = json.dumps(dados_trusted)
print(json_trusted)

session = boto3.Session()

s3 = session.client('s3')



s3.put_object(Body=json_trusted,Bucket=bucket_trusted,Key=file_name)

new_df_refined = df.select(df.Body.nomePaciente.alias('nome_paciente'),
                           df.Body.idadePaciente.alias('idadePaciente'),
                           df.Body.generoPaciente.alias('generoPaciente'),
                           df.Body.frequenciaCardiaca.alias('frequenciaCardiaca'),
                           df.Body.dataLeitura.alias('dataLeitura'))


new_df_refined.show()

dados_refined = new_df_refined.collect()


json_refined = json.dumps(dados_refined)
print(json_refined)



s3.put_object(Body=json_refined,Bucket=bucket_refined,Key=file_name)
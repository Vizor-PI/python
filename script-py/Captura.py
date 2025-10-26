import pandas as pd
import psutil
import time
import datetime
import os
import logging
#import boto3
#from botocore.exceptions
#import ClientError 
import os


def get_temperatura_cpu():
    """Captura a temperatura da CPU (funciona no Linux)."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "Nao disponivel"
        for nome, entradas in temps.items():
            for e in entradas:
                label = e.label.lower() if e.label else nome.lower()
                if "cpu" in label or "core" in label:
                    return round(e.current, 1)
        primeira = list(temps.values())[0][0].current
        return round(primeira, 1)
    except Exception:
        return "Nao disponivel"

def get_temperatura_cpu_windows():
    """Captura temperatura da CPU em Windows (usando WMI)."""
    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
        temperature_info = w.MSAcpi_ThermalZoneTemperature()
        if temperature_info:
            temp_celsius = (temperature_info[0].CurrentTemperature / 10.0) - 273.15
            return round(temp_celsius, 1)
        return "Nao disponivel"
    except Exception:
        return "Nao disponivel"

def get_uptime_formatado():
    """Retorna o tempo ligado formatado como 'Xh Ymin'."""
    tempo_boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    agora = datetime.datetime.now()
    tempo_ligado = agora - tempo_boot
    segundos = tempo_ligado.total_seconds()
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    return f"{horas}h {minutos}min"



def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

dados = {
    "User": "None",
    "Timestamp": [],
    "CPU": [],
    "Memoria": [],
    "Disco":[],
    "Rede": [],
    "Processos": [],
    "Data_Boot": [],
    "uptime_min": [],
    "temperaturaCPU": [],
    "indoor": []
}
              # Alterar nome aqui (ex: COD003-Dados-da-Maquina.csv)
arquivo_csv = 'COD004-Dados-da-Maquina.csv'


def salvamento(valor):
    if valor == 1:
        dados = {
                    #Adicionar seu COD aqui
            "User": "COD004 ",
            "Timestamp": [data_hora],
            "CPU": [cpu],
            "Memoria": [memoria.percent],
            "Disco":[disco.percent],
            "Rede": [round((rede.bytes_recv/ 1024** 3),2)],
            "Processos": [quantidade],
            "Data_Boot": [dataBoot],
            "uptime_min": [uptime_min],
            "temperaturaCPU": [temperaturaCPU],
            "indoor": [0]
            }
        df = pd.DataFrame(dados)

                  # Alterar nome aqui (ex: COD003-Dados-da-Maquina.csv)
        df.to_csv("COD004-Dados-da-Maquina.csv", encoding="utf-8", index=False, sep=";")
    elif valor == 2:
        novalinha = {
                    #Adicionar seu COD aqui
            "User": "COD004 ",
            "Timestamp": [data_hora],
            "CPU": [cpu],
            "Memoria": [memoria.percent],
            "Disco":[disco.percent],
            "Rede": [round((rede.bytes_recv/ 1024** 3),2)],
            "Processos": [quantidade],
            "Data_Boot": [dataBoot],
            "uptime_min": [uptime_min],
            "temperaturaCPU": [temperaturaCPU],
            "indoor": [0]
            }
        adicionar = pd.DataFrame(novalinha)
        maisdados = pd.concat([leitor,adicionar])

                        # Alterar nome aqui (ex: COD003-Dados-da-Maquina.csv)
        maisdados.to_csv("COD004-Dados-da-Maquina.csv",encoding="utf-8", index=False, sep=";")

while True:
    #parte das varíaveis
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=None, percpu=False)
    rede = psutil.net_io_counters(pernic=False, nowrap=True)
    dataBoot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    
    #Parte dos processos
    quantidade = 0
    for processos in psutil.process_iter(['pid','name','username']):
        quantidade+=1
    
    # Calcular uptime formatado
    uptime_min = get_uptime_formatado()

    # Capturar temperatura da CPU com fallback para Windows
    temperaturaCPU = get_temperatura_cpu()
    if temperaturaCPU == "Nao disponivel" and os.name == "nt":
        temperaturaCPU = get_temperatura_cpu_windows()


    #Parte de salvamento
    if os.path.exists(arquivo_csv):
        try:
                                ## Alterar nome aqui (ex: COD003-Dados-da-Maquina.csv)
            leitor = pd.read_csv('COD004-Dados-da-Maquina.csv', sep=";")
            if not leitor.empty:
                print("Csv não está vazio")
                salvamento(2)
                
        except pd.errors.EmptyDataError:
            print("Está vazio ou não contém dados")
            salvamento(1)
    else:
        salvamento(1)
        print("Está vazio ou não contém dados")

    #Exibições
    print("_"*50)

    print(f"Data e hora atual: {data_hora} \nDisco usado: {disco.percent}% \nMemória usada: {memoria.percent}% \nCPU usada: {cpu}% \nQuantidade de processos: {quantidade} \nRede (bytes recebidos):{rede.bytes_recv} \nData do Ultimo boot: {dataBoot} \nTemperatura CPU: {temperaturaCPU}°C \nTempo ligado: {uptime_min}")
   

    print("_"*50)

    time.sleep(10)

    # Só funciona dentro da VM (salva no bucket):
    # upload_file('Dados-da-Maquina.csv', 'raw-lucasaquino')
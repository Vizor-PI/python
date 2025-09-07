import pandas as pd
import psutil
import time
import datetime
import os

dados = {
    "User": "None",
    "Timestamp": [],
    "CPU": [],
    "Memória": [],
    "Disco":[],
    "Rede": [],
    "Data_Boot": []
}
arquivo_csv = 'Dados-da-Maquina.csv'


def salvamento(valor):
    if valor == 1:
        dados = {
            "User": "Vizor",
            "Timestamp": [data_hora],
            "CPU": [cpu],
            "Memória": [memoria.percent],
            "Disco":[disco.percent],
            "Rede": [round((rede.bytes_recv/ 1024** 3),2)],
            "Data_Boot": [dataBoot]
            }
        df = pd.DataFrame(dados)
        df.to_csv("Dados-da-Maquina.csv", encoding="utf-8", index=False, sep=";")
    elif valor == 2:
        novalinha = {
            "User": "Vizor",
            "Timestamp": [data_hora],
            "CPU": [cpu],
            "Memória": [memoria.percent],
            "Disco":[disco.percent],
            "Rede": [round((rede.bytes_recv/ 1024** 3),2)],
            "Data_Boot": [dataBoot]
            }
        adicionar = pd.DataFrame(novalinha)
        maisdados = pd.concat([leitor,adicionar])
        maisdados.to_csv("Dados-da-Maquina.csv",encoding="utf-8", index=False, sep=";")

while True:
    #parte das varíaveis
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    cpu = psutil.cpu_percent(interval=None, percpu=False);
    rede = psutil.net_io_counters(pernic=False, nowrap=True)
    dataBoot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    #Parte dos processos
    quantidade = 0
    for processos in psutil.process_iter(['pid','name','username']):
        quantidade+=1

    #Parte de salvamento
    if os.path.exists(arquivo_csv):
        try:
            leitor = pd.read_csv('Dados-da-Maquina.csv', sep=";")
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
    print("_"*30)
    print(f"Data e hora atual: {data_hora} disco usado: {disco.percent}% Memória usada {memoria.percent}% Frêquencia atual: {cpu}%, Rede: Data do Ultimo boot: ")

    print("_"*30)
    time.sleep(10)
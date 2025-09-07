# Monitoramento de Métricas do Sistema

Este projeto contém um script em **Python** que coleta métricas de uso do sistema utilizando as bibliotecas [psutil](https://pypi.org/project/psutil/) e [pandas](https://pandas.pydata.org/).  
As informações são salvas em um arquivo **CSV**, permitindo o acompanhamento histórico de desempenho.

---

## Funcionalidades

- **CPU** → Uso percentual.  
- **Memória RAM** → Total, usada e percentual de uso.  
- **Disco** → Capacidade total, espaço usado e percentual de uso.  
- **Rede** → Bytes enviados e recebidos.  
- **Último boot** → Data e hora da última inicialização do sistema.  
- **Timestamp da coleta** → Momento em que os dados foram registrados.  

---

## Saída

Os dados coletados são organizados em um **DataFrame** do *pandas* e exportados para o arquivo:

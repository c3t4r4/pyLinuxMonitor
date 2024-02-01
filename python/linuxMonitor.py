import psutil
import requests
import time
import socket
from datetime import datetime
import config  # Importa o arquivo de configuração

# Obtém o hostname da máquina
hostname = socket.gethostname()

def get_system_info():
    # Coleta informações de CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_total = psutil.cpu_count(logical=True)  # Total de CPUs
    
    # Coleta informações de memória
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    ram_total = memory.total / (1024**3)  # Convertendo bytes para GB
    
    # Coleta informações do disco (múltiplos discos podem ser adicionados)
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    disk_total = disk.total / (1024**3)  # Convertendo bytes para GB
    
    return {
        'id': config.UNIQUE_ID,
        'hostname': hostname,
        'cpu_usage': cpu_usage,
        'cpu_total': cpu_total,
        'ram_usage': ram_usage,
        'ram_total': ram_total,
        'disk_usage': disk_usage,
        'disk_total': disk_total,
        'timestamp': datetime.now().isoformat()
    }

def post_data(data):
    try:
        # Usa a URL do arquivo de configuração
        response = requests.post(config.api_url, json=data)
        response.raise_for_status()
        print(f'Dados enviados com sucesso: {data}')
    except requests.exceptions.HTTPError as err:
        print(f'Erro ao enviar dados: {err}')

def main():
    while True:
        system_info = get_system_info()
        post_data(system_info)
        time.sleep(60)

if __name__ == "__main__":
    main()

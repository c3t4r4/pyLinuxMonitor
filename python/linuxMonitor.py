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
    
    # Coleta informações de memória
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    
    # Coleta informações do disco (múltiplos discos podem ser adicionados)
    disk_usage = psutil.disk_usage('/').percent
    
    return {
        'id': config.unique_id,
        'key': config.api_key,
        'hostname': hostname,
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'disk_usage': disk_usage,
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

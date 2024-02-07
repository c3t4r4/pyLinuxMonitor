import psutil
import requests
import time
import socket
import json
from datetime import datetime
import config  # Importa o arquivo de configuração

# Obtém o hostname da máquina
hostname = socket.gethostname()


def get_largest_partition_info():
    partitions_info = {}

    for part in psutil.disk_partitions(all=False):
        if 'cdrom' in part.opts or part.fstype == '':
            continue
        usage = psutil.disk_usage(part.mountpoint)
        # Corrigindo a extração do identificador do disco
        disk_base = ''.join(filter(str.isalpha, part.device))

        for i, c in enumerate(part.device):
            if c.isdigit():
                disk_base = part.device[:i + 1]  # Inclui até o primeiro dígito
                break

        # Se o disco ainda não está no dicionário ou se esta partição é maior, atualiza
        if disk_base not in partitions_info or usage.total > partitions_info[disk_base]['total']:
            if usage.total / (1024 ** 3) > 10:
                partitions_info[disk_base] = {
                    'disk': part.device,
                    'usage_percent': usage.percent,
                    'total': usage.total / (1024 ** 3),
                    'total_gb': "{:.2f}".format(usage.total / (1024 ** 3)),  # Convertendo para GB
                    'used_gb': "{:.2f}".format(usage.used / (1024 ** 3))  # Convertendo para GB
                }

    return list(partitions_info.values())

def get_system_info():
    # Coleta informações de CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_total = psutil.cpu_count(logical=True)  # Total de CPUs

    # Coleta informações de memória
    memory = psutil.virtual_memory()
    ram_usage = "{:.2f}".format(memory.percent)
    ram_total = "{:.2f}".format(memory.total / (1024 ** 3))  # Convertendo bytes para GB

    # Inicializa listas para armazenar informações de cada disco
    discos = get_largest_partition_info()


    return {
        "node_id": config.unique_id,
        "key": config.api_key,
        "hostname": hostname,
        "cpu_usage": cpu_usage,
        "cpu_total": cpu_total,
        "ram_usage": ram_usage,
        "ram_total": ram_total,
        "disks": discos,
        "timestamp": datetime.now().isoformat()
    }


def post_data(data):
    json_data = json.dumps(data)  # Convertendo o dicionário Python para uma string JSON
    headers = {'Content-Type': 'application/json'}

    try:
        # Usa a URL do arquivo de configuração
        response = requests.post(config.api_url, data=json_data, headers=headers)
        response.raise_for_status()
        print(f'Dados enviados com sucesso: {data}')
    except requests.exceptions.HTTPError as err:
        print(json_data)
        print(f'Erro ao enviar dados: {err}')


def main():
    while True:
        system_info = get_system_info()
        post_data(system_info)
        time.sleep(60)


if __name__ == "__main__":
    main()

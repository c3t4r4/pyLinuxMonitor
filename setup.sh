#!/bin/bash

# Definindo variáveis
SCRIPT_URL="https://raw.githubusercontent.com/c3t4r4/pyLinuxMonitor/main/python/linuxMonitor.py"
SCRIPT_DIR="/opt/pyLinuxMonitor"
SCRIPT_NAME="linuxMonitor.py"
CONFIG_FILE_NAME="config.py"

# Cria o diretório, se não existir
mkdir -p $SCRIPT_DIR

# Baixa o script Python do GitHub
curl -o $SCRIPT_DIR/$SCRIPT_NAME $SCRIPT_URL

# Instala as dependências
python3 -m pip install psutil requests

# Gera um ID único
unique_id=$(uuidgen)

# Coleta a URL da API e a API Key do usuário
read -p "Insira a URL da API: " api_url
read -p "Insira a API Key: " api_key

# Salva as configurações no arquivo config.py no diretório do script
echo "unique_id = '$unique_id'" > $SCRIPT_DIR/$CONFIG_FILE_NAME
echo "api_url = '$api_url'" >> $SCRIPT_DIR/$CONFIG_FILE_NAME
echo "api_key = '$api_key'" >> $SCRIPT_DIR/$CONFIG_FILE_NAME

# Dá permissão de execução ao script Python
chmod +x $SCRIPT_DIR/$SCRIPT_NAME

# Cria um serviço systemd para o script
SERVICE_FILE="/etc/systemd/system/pyLinuxMonitor.service"

echo "[Unit]
Description=pyLinuxMonitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_DIR/$SCRIPT_NAME
WorkingDirectory=$SCRIPT_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE

# Recarrega os serviços systemd, inicia e habilita o serviço
sudo systemctl daemon-reload
sudo systemctl start pyLinuxMonitor.service
sudo systemctl enable pyLinuxMonitor.service

echo "Script configurado e serviço iniciado com sucesso!"

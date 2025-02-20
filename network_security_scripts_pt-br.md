
## Traduções Disponíveis
- 🇧🇷 Português (Atual)
- 🇺🇸 [Inglês](network_security_scripts.md)


# Documentação dos Scripts de Segurança de Rede

## Visão Geral
Esta documentação fornece uma explicação sobre três scripts principais usados em um sistema de segurança de rede.  
Cada script tem uma função específica: monitorar o tráfego da rede, detectar IPs suspeitos e bloquear IPs maliciosos.

---

## 1. Script de Monitoramento de Rede (`network_monitor.py`)

### Objetivo
- Este script monitora o tráfego da rede em tempo real.
- Ele registra os pacotes detectados, registrando sua origem, destino e tamanho.
- Atua como uma câmera de segurança observando toda a atividade da rede.

### Como Funciona
- Usa o Scapy para capturar pacotes da rede.
- Se um pacote contiver uma camada IP, ele registra os detalhes.
- Armazena todos os logs de pacotes em um arquivo: `packet_log.txt`.

### Explicação do Código
```python
from datetime import datetime
from scapy.all import sniff
from scapy.layers.inet import IP

LOG_FILE = "packet_log.txt"

def monitor_packet(packet):
    """
    Analisa pacotes de rede e registra o tráfego de IP detectado.
    """
    if packet.haslayer(IP):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        packet_size = len(packet)

        log_entry = (
            f"[{timestamp}] Pacote detectado: {src_ip} -> {dst_ip} "
            f"| Tamanho: {packet_size} bytes\n"
        )

        print(log_entry.strip())  # Exibir no console

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_entry)

print("Iniciando monitoramento da rede em tempo real...")
sniff(prn=monitor_packet, store=False, filter="ip")  # Captura apenas pacotes IP
```

### Exemplo de Saída
```
[2024-02-20 10:30:45] Pacote detectado: 192.168.1.10 -> 8.8.8.8 | Tamanho: 64 bytes
[2024-02-20 10:30:47] Pacote detectado: 192.168.1.20 -> 192.168.1.1 | Tamanho: 128 bytes
```

---

## 2. Script de Detecção de IPs Suspeitos (`detect_suspicious_ips.py`)

### Objetivo
- Este script analisa os logs de tráfego da rede para encontrar IPs suspeitos.
- Se um IP fizer muitas solicitações, ele será marcado como suspeito.
- Armazena os IPs suspeitos em um arquivo: `suspicious_ips.csv`.

### Como Funciona
- Carrega os dados de tráfego da rede a partir de `network_data.csv`.
- Define um limite de solicitações (por exemplo, mais de 1000 solicitações é suspeito).
- Filtra os IPs que ultrapassam o limite e os registra.

### Explicação do Código
```python
import os
import pandas as pd

DATA_FILE = "network_data.csv"
SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "suspicious_activity.log"

if not os.path.exists(DATA_FILE):
    print(f"Erro: {DATA_FILE} não encontrado! Verifique o caminho do arquivo.")
    exit()

df = pd.read_csv(DATA_FILE)

REQUEST_THRESHOLD = 1000

suspicious_traffic = df[df["request_count"] > REQUEST_THRESHOLD]

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write("\nIPs suspeitos detectados:\n")
    for index, row in suspicious_traffic.iterrows():
        log_entry = f"{row['ip_address']} - {row['request_count']} solicitações\n"
        print(log_entry.strip())  
        log.write(log_entry)

suspicious_traffic[["ip_address"]].to_csv(SUSPICIOUS_IPS_FILE, index=False)

print(f"IPs suspeitos salvos em {SUSPICIOUS_IPS_FILE}")
```

### Exemplo de Saída
```
IPs suspeitos detectados:
203.0.113.15 - 1500 solicitações
192.168.1.100 - 1800 solicitações
IPs suspeitos salvos em suspicious_ips.csv
```

---

## 3. Script de Bloqueio de IPs (`block_suspicious_ips.py`)

### Objetivo
- Este script bloqueia os IPs que foram marcados como suspeitos.
- Usa iptables (firewall do Linux) para impedir mais acessos.
- Armazena os IPs bloqueados em `blocked_ips.log`.

### Como Funciona
- Carrega os IPs suspeitos a partir de `suspicious_ips.csv`.
- Verifica se um IP já está bloqueado para evitar duplicações.
- Adiciona uma regra de firewall (`iptables -A INPUT -s <IP> -j DROP`).
- Registra os IPs bloqueados em `blocked_ips.log`.

### Explicação do Código
```python
import os
import pandas as pd

SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "blocked_ips.log"

if not os.path.exists(SUSPICIOUS_IPS_FILE):
    print(f"Erro: {SUSPICIOUS_IPS_FILE} não encontrado! Verifique o caminho do arquivo.")
    exit()

suspicious_ips_df = pd.read_csv(SUSPICIOUS_IPS_FILE)
suspicious_ip_list = suspicious_ips_df["ip_address"].tolist()

def is_ip_blocked(ip_address):
    result = os.popen(f"iptables -L INPUT -v -n | grep {ip_address}").read()
    return bool(result)

def block_ip(ip_address):
    if is_ip_blocked(ip_address):
        print(f"Ignorando {ip_address} (já bloqueado).")
        return

    print(f"Bloqueando IP: {ip_address}")
    os.system(f"iptables -A INPUT -s {ip_address} -j DROP")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{ip_address} bloqueado\n")

for suspicious_ip in suspicious_ip_list:
    block_ip(suspicious_ip)

print("Todos os IPs suspeitos foram bloqueados.")
```

### Exemplo de Saída
```
Bloqueando IP: 203.0.113.15
Bloqueando IP: 192.168.1.100
Todos os IPs suspeitos foram bloqueados.
```

---

## Como Executar os Scripts

### Etapa 1: Monitorar o Tráfego da Rede
```bash
python network_monitor.py
```

### Etapa 2: Detectar IPs Suspeitos
```bash
python detect_suspicious_ips.py
```

### Etapa 3: Bloquear IPs Suspeitos
```bash
sudo python block_suspicious_ips.py
```

---

## Resumo dos Scripts

| Script | Função | Arquivo de Saída |
|--------|--------|-----------------|
| `network_monitor.py` | Monitora o tráfego de rede em tempo real | `packet_log.txt` |
| `detect_suspicious_ips.py` | Detecta IPs suspeitos (alto volume de requisições) | `suspicious_ips.csv` |
| `block_suspicious_ips.py` | Bloqueia IPs maliciosos via firewall | `blocked_ips.log` |

---

## Conclusão

- Esses três scripts trabalham juntos para monitorar, detectar e bloquear atividades maliciosas na rede.
- O monitoramento em tempo real ajuda a rastrear atividades, enquanto a análise de logs identifica ameaças.
- As regras do firewall garantem que IPs suspeitos não tenham acesso à rede.

---
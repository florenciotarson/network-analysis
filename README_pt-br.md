```markdown

## Traduções disponíveis
- 🇬🇧 [English](README.md)
- 🇧🇷 Português (Atual)

# Análise de Rede

> **Análise Exploratória de Dados & Avaliação de Riscos para Tráfego de Rede**

Bem-vindo ao **Projeto de Análise de Rede & Avaliação de Riscos**!  
Este repositório foca na **análise exploratória de dados (EDA)** e na **avaliação de riscos de segurança** para dados de tráfego de rede, fornecendo uma abordagem abrangente para identificar ameaças e mitigar vulnerabilidades.

---

## **Índice**

1. [Introdução](#introdução)
2. [Objetivos do Projeto](#objetivos-do-projeto)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Instalação e Uso](#instalação-e-uso)
5. [Painel de Segurança (`security_dashboard.py`)](#painel-de-segurança-security_dashboardpy)
6. [Política de Segurança e Estratégias de Mitigação](#política-de-segurança-e-estratégias-de-mitigação)
7. [Contato e Considerações Finais](#contato-e-considerações-finais)

---

## **Introdução**

> Este projeto demonstra **análise de dados**, **raciocínio lógico** e **identificação e mitigação de riscos de segurança**.  
> Os principais focos incluem:

1. **Análise de Dados**  
   - Explorar dados de tráfego de rede para detectar possíveis riscos de segurança.  
   - Fornecer insights detalhados por meio da análise de dados.

2. **Identificação de Riscos e Desenvolvimento de Políticas de Segurança**  
   - Identificar **padrões de ameaças**, anomalias e atividades suspeitas.  
   - Propor uma **política de segurança acionável** com base nas descobertas.

3. **Implementação e Automação**  
   - Desenvolver soluções para mitigar riscos identificados.  
   - Automatizar **detecção de riscos** e gerar **relatórios de segurança**.

---

## **Objetivos do Projeto**

1. **Análise Exploratória de Dados (EDA)**  
   - Realizar uma **exploração profunda** dos logs de tráfego de rede.  
   - Identificar **padrões, anomalias e ameaças potenciais**.  
   - Resumir descobertas importantes em relatórios e visualizações.

2. **Avaliação de Riscos de Segurança e Recomendações de Política**  
   - Identificar **comportamentos suspeitos** (ex: alto volume de requisições, grandes transferências de dados).  
   - Desenvolver **estratégias de mitigação** baseadas em insights de dados.  
   - Documentar políticas de segurança para um gerenciamento eficaz de riscos.

3. **Implementação e Relatórios**  
   - Criar **scripts** para automatizar avaliações de segurança.  
   - Gerar **relatórios HTML** resumindo riscos e descobertas.  
   - Fornecer recomendações claras para melhorar a **postura de segurança**.

---

## **Estrutura do Projeto**

O repositório está organizado da seguinte forma:

```bash
network-analysis/
├── data/
│   └── network_data.csv              # Conjunto de dados de tráfego de rede
├── notebooks/
│   └── exploratory_analysis.ipynb    # Jupyter notebook para EDA
├── scripts/
│   ├── __init__.py                   # Torna 'scripts' um pacote Python
│   ├── config.py                     # Arquivo de configuração (caminhos, limites)
│   ├── data_exploration.py           # Script de EDA básico (exibe informações e estatísticas)
│   ├── eda.py                        # Realiza EDA estatístico e visual
│   ├── exploratory_analysis.py        # Script de EDA via linha de comando
│   ├── pipeline.py                   # Executa todo o pipeline (EDA + análise de riscos + relatórios)
│   ├── report_generator.py           # Gera relatórios HTML
│   ├── risk_analysis.py              # Identifica atividades suspeitas nos logs de tráfego
│   └── security_dashboard.py          # Painel de Segurança interativo via Streamlit
├── README.md
├── requirements.txt                   # Dependências
└── security_report.html                # Relatório de segurança
```

---

## **Arquivos Principais**

- **`config.py`** → Define constantes (caminhos de arquivos, limites).  
- **`pipeline.py`** → Automatiza o processamento de dados, análise e geração de relatórios.  
- **`report_generator.py`** → Compila os resultados em um relatório HTML.  
- **`risk_analysis.py / risk_analysis_2.py`** → Detecta riscos de segurança.  
- **`exploratory_analysis.py`** → Fornece insights rápidos de dados via linha de comando.  

---

## **Instalação e Uso**

### **🔹 Passo 1: Clonar o repositório**

```bash
git clone https://github.com/florenciotarson/network-analysis.git
cd network-analysis
```

### **🔹 Passo 2: Instalar dependências**

```bash
pip install -r requirements.txt
```

### **🔹 Passo 3: Preparar os dados**

Certifique-se de que o arquivo `network_data.csv` está dentro da pasta `data/`.  
Caso contrário, **atualize o caminho do arquivo no `config.py`**.

### **🔹 Passo 4: Executar o painel de segurança**
```bash
streamlit run security_dashboard.py
```

Isso irá:
- Iniciar um **painel interativo do Streamlit**.
- Exibir **IPs suspeitos, tamanhos de requisição incomuns e atividades fora do horário comercial**.
- **Exibir gráficos, tabelas e resumos dos dados**.

### **🔹 Passo 5: Exploração básica dos dados**
```bash
python -m scripts.data_exploration
```

Isso irá:
- **Carregar e inspecionar o conjunto de dados**.
- Exibir **estatísticas resumidas** (ex: média, mediana, mínimo, máximo, desvio padrão).
- Mostrar **tipos de dados e verificar valores ausentes**.

### **🔹 Passo 6: Executar a análise exploratória**
```bash
python -m scripts.exploratory_analysis
```

Isso irá:
- Identificar **IPs suspeitos, tamanhos de requisição incomuns e atividades fora do horário comercial**.
- Gerar **visualizações básicas** (histograma, distribuição geográfica, tendências ao longo do tempo).

### **🔹 Passo 7: Realizar análise de risco**
```bash
python -m scripts.risk_analysis
```

Isso irá:
- Identificar **IPs suspeitos**, **tamanhos de requisição incomuns** e **atividade fora do horário comercial**.
- Exibir **resumos de risco** e descobertas relevantes no console.

(Como alternativa, você pode testar `risk_analysis_2.py` para uma abordagem ligeiramente diferente:)
```bash
python -m scripts.risk_analysis_2
```

Isso irá:
- Verificar **contagens de requisições de IPs, requisições incomuns e tráfego fora do horário comercial**.
- Exibir um **resumo conciso das atividades suspeitas no console**.
- Perfeito para **validar rapidamente mudanças nos limites ou focar em um conjunto mais específico de indicadores de segurança**.

### **🔹 Passo 8: Gerar um relatório de segurança**
```bash
python -m scripts.pipeline
```

Isso irá:
- Executar **EDA + Análise de Risco**.
- Criar um **arquivo security_report.html** com todas as descobertas.


## **6. Política de Segurança e Estratégias de Mitigação**

### ** 1. Atividade Suspeita de IPs**

| Risco | Mitigação |
|-------|-----------|
| Alto volume de requisições de um único IP | Implementar **limitação de taxa** e **bloqueio de IPs** |
| Requisições repetidas de locais desconhecidos | Usar **filtros de geolocalização** e **mecanismos de autenticação** |

### ** 2. Transferências de Dados Incomuns**

| Risco | Mitigação |
|-------|-----------|
| Requisições com tamanho anormalmente alto | **Monitorar tamanhos de requisição** e alertar sobre anomalias |
| Comportamento incomum de upload/download | **Definir limites** e **restringir endpoints sensíveis** |

### ** 3. Tráfego Fora do Horário Comercial**

| Risco | Mitigação |
|-------|-----------|
| Alto tráfego fora do horário comercial | Marcar como **atividade fora do padrão** |
| Possíveis tentativas de acesso não autorizado | Usar **logs de acesso** e **análise de comportamento do usuário** |

### **4. Padrões de Tráfego Anômalos**
| Risco | Mitigação |
|-------|-----------|
| Picos repentinos no tráfego | Detectar **atividade semelhante a DDoS** e aplicar **controles de taxa** |
| Métodos HTTP incomuns ou códigos de erro elevados | Monitorar **potenciais ataques** e aplicar **regras de firewall** |


---

## **7. Próximos Passos**
# Ampliar a Análise:
- Identificar anomalias mais avançadas e padrões de ataque.
- Melhorar a detecção de riscos utilizando modelos de aprendizado de máquina.

# Automatizar Relatórios:
- Aprimorar o gerador de relatórios HTML com mais visualizações.
- Integrar com ferramentas SIEM para alertas de segurança.

# Reforçar Políticas de Segurança:
- Implementar monitoramento proativo de riscos e respostas automatizadas.
- Desenvolver um pipeline de detecção de riscos em tempo real.

---

## **8. Licença e Atribuição**
Este projeto é de propriedade da Oxecollective Consulting.  
O uso é permitido para fins de aprendizado e avaliação interna de segurança.

Aviso:  
Este projeto é para fins educacionais e de pesquisa.  
Ele não substitui soluções ou políticas profissionais de segurança.


---

## **9. Contato**
Para dúvidas, entre em contato via **[Oxecollective Consulting](http://www.oxecollective.com)**.

---

## ** Recursos Relacionados**

- [OWASP Práticas de Segurança](https://owasp.org/)  
- [MITRE ATT&CK Framework](https://attack.mitre.org/)  
- [Diretrizes de Segurança SANS](https://www.sans.org/)  

---

## Considerações Finais

> Este projeto fornece uma **base sólida** para análise de segurança de redes.  
> **Continue iterando e aprimorando os mecanismos de detecção de riscos para uma infraestrutura mais segura!**  
>  
> [www.oxecollective.com](http://www.oxecollective.com)

```

www.oxecollective.com
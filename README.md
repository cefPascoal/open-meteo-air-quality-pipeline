# Open-Meteo Air Quality Pipeline

Pipeline de Engenharia de Dados para ingestão, transformação, validação e persistência de dados de qualidade do ar provenientes da API do [Open-Meteo](https://open-meteo.com/).

O projeto foi desenvolvido como um **projeto de portfólio de Engenharia de Dados**, com foco em demonstrar boas práticas de organização de código, separação de responsabilidades, qualidade de dados, tratamento de registros inválidos, testes automatizados e execução operacional.

---

## Objetivo

Construir uma pipeline capaz de:

* consumir dados de qualidade do ar através de uma API;
* suportar múltiplas localizações;
* transformar a resposta da API em registros tabulares;
* validar a qualidade dos dados;
* encaminhar registros válidos para saída;
* encaminhar registros inválidos para quarantine;
* persistir os resultados em formato JSONL;
* testar individualmente as principais camadas;
* executar a pipeline através de um script operacional;
* registrar a execução em arquivo de log.

---

## Arquitetura

A pipeline segue uma arquitetura simples, modular e orientada à separação de responsabilidades:

```text
Open-Meteo API
      │
      ▼
 API Client
      │
      ▼
  Ingestion
      │
      ▼
Transformation
      │
      ▼
  Validation
      │
      ├───────────────┐
      │               │
    válido          inválido
      │               │
      ▼               ▼
   Output         Quarantine
      │               │
      ▼               ▼
 air_quality.jsonl  quarantine.jsonl
```

A execução é coordenada pela camada de **Orchestration**, que determina o destino de cada registro após a validação.

---

## Estrutura do projeto

```text
open-meteo-air-quality-pipeline/
│
├── config/
│   ├── locations.yaml
│   └── pipeline.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── air_quality.jsonl
│       └── quarantine.jsonl
│
├── logs/
│   └── pipeline.log
│
├── scripts/
│   └── run_pipeline.bat
│
├── src/
│   ├── api/
│   │   └── open_meteo.py
│   ├── ingestion/
│   │   └── air_quality.py
│   ├── transformation/
│   │   └── air_quality.py
│   ├── validation/
│   │   └── air_quality.py
│   ├── quarantine/
│   │   └── air_quality.py
│   ├── output/
│   │   └── air_quality.py
│   ├── orchestration/
│   │   └── air_quality.py
│   ├── data_quality.py
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── test_api.py
│   ├── test_config.py
│   ├── test_data_quality.py
│   ├── test_ingestion.py
│   ├── test_orchestration.py
│   ├── test_output.py
│   ├── test_quarantine.py
│   ├── test_transformation.py
│   └── test_validation.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

# Tecnologias

* Python 3.12+
* pytest
* httpx
* PyYAML
* JSONL
* Git / GitHub
* Windows Batch Script

A pipeline foi mantida propositalmente simples, sem introduzir ferramentas de orquestração distribuída ou infraestrutura cloud que não sejam necessárias para o objetivo deste projeto.

---

# Configuração

A configuração da pipeline é separada do código através de arquivos YAML.

## Pipeline

Arquivo:

```text
config/pipeline.yaml
```

Exemplo:

```yaml
pipeline:
  name: air-quality-ingestion
  version: 1

source:
  name: open-meteo-air-quality
  base_url: ${OPEN_METEO_BASE_URL}

period:
  start_date: "2026-01-01"
  end_date: "2026-06-30"

variables:
  - pm10
  - pm2_5
  - carbon_monoxide
  - nitrogen_dioxide
  - ozone
  - dust
  - aerosol_optical_depth
```

## Localizações

Arquivo:

```text
config/locations.yaml
```

Atualmente são configuradas três localizações:

* Luanda — Angola
* Lisbon — Portugal
* Beijing — China

Cada localização possui:

* nome;
* país;
* latitude;
* longitude;
* timezone.

Exemplo:

```yaml
locations:
  - name: Luanda
    country: Angola
    latitude: -8.8390
    longitude: 13.2894
    timezone: Africa/Luanda
```

---

# Variável de ambiente

A URL da API é definida através da variável:

```text
OPEN_METEO_BASE_URL
```

O projeto fornece um exemplo em:

```text
.env.example
```

Conteúdo:

```text
OPEN_METEO_BASE_URL=https://air-quality-api.open-meteo.com/v1/air-quality
```

A aplicação utiliza a variável existente no ambiente de execução.

No Git Bash:

```bash
export OPEN_METEO_BASE_URL=https://air-quality-api.open-meteo.com/v1/air-quality
```

No PowerShell:

```powershell
$env:OPEN_METEO_BASE_URL="https://air-quality-api.open-meteo.com/v1/air-quality"
```

---

# Instalação

Clone o repositório:

```bash
git clone git@github.com:cefPascoal/open-meteo-air-quality-pipeline.git
```

Entre no projeto:

```bash
cd open-meteo-air-quality-pipeline
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Git Bash:

```bash
source .venv/Scripts/activate
```

No PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -e .
```

---

# Execução

Depois de configurar a variável de ambiente, a pipeline pode ser executada diretamente através do módulo principal:

```bash
python -m src.main
```

A execução realiza as seguintes etapas:

```text
Configuração
    ↓
Cliente da API
    ↓
Ingestão
    ↓
Transformação
    ↓
Validação
    ↓
Orquestração
    ├── registros válidos
    │       ↓
    │   Output JSONL
    │
    └── registros inválidos
            ↓
        Quarantine JSONL
```

---

# Execução através do script

O projeto também possui um script operacional:

```text
scripts/run_pipeline.bat
```

No Windows/Git Bash:

```bash
./scripts/run_pipeline.bat
```

O script:

1. posiciona a execução na raiz do projeto;
2. verifica a variável `OPEN_METEO_BASE_URL`;
3. cria a pasta de logs quando necessário;
4. executa o ambiente Python do projeto;
5. executa a pipeline;
6. registra o resultado da execução.

Exemplo:

```text
Pipeline executado com sucesso.
```

---

# Logs

As execuções realizadas através do script são registradas em:

```text
logs/pipeline.log
```

Exemplo:

```text
[29/09/2026  9:55:57,54] Inicio do pipeline
[29/09/2026  9:56:06,46] Pipeline executado com sucesso.
```

Os logs são mantidos fora do controle de versão.

Isso evita versionar arquivos gerados durante a execução da pipeline.

---

# Dados de saída

Os resultados processados são armazenados em:

```text
data/processed/
```

## Dados válidos

Arquivo:

```text
data/processed/air_quality.jsonl
```

Cada linha representa um registro independente em formato JSON.

Exemplo:

```json
{
  "location": "Luanda",
  "country": "Angola",
  "latitude": -8.799995,
  "longitude": 13.300003,
  "timezone": "Africa/Luanda",
  "timestamp": "2026-01-01T00:00",
  "pm10": 14.0,
  "pm2_5": 10.5,
  "carbon_monoxide": 159.0,
  "nitrogen_dioxide": 3.3,
  "ozone": 47.0,
  "dust": 0.0,
  "aerosol_optical_depth": 0.11
}
```

## Quarantine

Registros que não atendem às regras de validação são encaminhados para:

```text
data/processed/quarantine.jsonl
```

Cada registro armazenado na quarantine contém:

```json
{
  "record": {},
  "errors": []
}
```

Dessa forma, o registro original é preservado juntamente com os erros encontrados.

---

# Validação de dados

A camada de validação verifica os principais campos necessários para a pipeline.

### Timestamp

O timestamp deve:

* existir;
* possuir formato ISO 8601 válido.

### Latitude

Deve estar entre:

```text
-90 e 90
```

### Longitude

Deve estar entre:

```text
-180 e 180
```

### PM10

Deve existir e possuir valor maior ou igual a zero.

### PM2.5

Deve existir e possuir valor maior ou igual a zero.

### Carbon Monoxide

Deve existir e possuir valor maior ou igual a zero.

Quando um registro possui múltiplos problemas, os erros são acumulados:

```json
{
  "valid": false,
  "errors": [
    "Invalid latitude",
    "Invalid pm10"
  ]
}
```

---

# Testes

O projeto utiliza `pytest` para testes automatizados.

Executar toda a suíte:

```bash
python -m pytest
```

Executar com saída resumida:

```bash
python -m pytest -q
```

Os testes cobrem as principais camadas do projeto:

* configuração;
* cliente da API;
* retries e tratamento de erros;
* ingestão;
* transformação;
* validação;
* quarantine;
* persistência;
* output;
* orchestration;
* integração;
* qualidade dos dados.

A quantidade de testes pode evoluir à medida que novas regras ou componentes sejam adicionados.

---

# Qualidade dos dados

Além da validação individual dos registros, o projeto possui verificações simples sobre os dados produzidos.

Entre elas:

* identificação das localizações presentes no output;
* identificação de localizações esperadas que não foram produzidas;
* verificação do período dos timestamps produzidos.

Essas verificações representam uma primeira camada de **Data Quality** após o processamento.

---

# Resiliência da API

O cliente da API possui mecanismos básicos de resiliência.

São tratados:

* timeout;
* erros de conexão;
* HTTP `429`;
* HTTP `500`;
* HTTP `502`;
* HTTP `503`;
* HTTP `504`.

Para erros que podem ser temporários, são realizadas novas tentativas utilizando backoff exponencial.

Exemplo:

```text
Tentativa 1
    ↓
aguarda 1 segundo
    ↓
Tentativa 2
    ↓
aguarda 2 segundos
    ↓
Tentativa 3
```

O número máximo de tentativas é configurável no cliente.

---

# Separação de responsabilidades

Uma das preocupações do projeto é evitar que uma única classe seja responsável por toda a pipeline.

As responsabilidades estão separadas da seguinte forma:

| Componente                 | Responsabilidade                        |
| -------------------------- | --------------------------------------- |
| `OpenMeteoClient`          | Comunicação com a API                   |
| `AirQualityIngestion`      | Ingestão dos dados                      |
| `AirQualityTransformation` | Transformação da resposta da API        |
| `AirQualityValidator`      | Validação dos registros                 |
| `AirQualityOrchestrator`   | Encaminhamento dos registros            |
| `AirQualityOutput`         | Persistência dos registros válidos      |
| `AirQualityQuarantine`     | Acumulação e persistência dos inválidos |
| `data_quality`             | Verificações sobre os dados produzidos  |
| `main.py`                  | Composição e execução da pipeline       |

Essa separação permite testar e evoluir cada componente de forma independente.

---

# Estratégia de tratamento de registros inválidos

Um registro inválido não interrompe automaticamente toda a execução.

O fluxo é:

```text
Registro
   ↓
Validação
   │
   ├── válido ──────► Output
   │
   └── inválido ────► Quarantine
```

Isso permite preservar os registros problemáticos para posterior análise sem necessariamente interromper o processamento dos demais dados.

---

# Execução e automação

A execução operacional foi separada da lógica da pipeline.

O script:

```text
scripts/run_pipeline.bat
```

funciona como ponto de entrada para uma execução automatizada.

Em um ambiente real, este script poderia ser acionado por diferentes mecanismos, dependendo da infraestrutura disponível, por exemplo:

```text
Scheduler
   ↓
run_pipeline.bat
   ↓
Python
   ↓
Pipeline
```

Ou:

```text
CI/CD
   ↓
Pipeline
```

Ou ainda por uma ferramenta de orquestração dedicada em ambientes que exijam maior complexidade operacional.

Neste projeto de portfólio, não foi adicionada uma ferramenta de scheduling ou orquestração distribuída apenas para aumentar a complexidade da solução.

---

# Decisões de projeto

Algumas decisões foram tomadas deliberadamente:

### JSONL como formato de saída

JSONL permite armazenar cada registro em uma linha independente, sendo simples para:

* processamento incremental;
* inspeção;
* testes;
* ingestão posterior em outros sistemas.

### YAML para configuração

A configuração de períodos, variáveis e localizações foi separada do código para facilitar alterações sem modificar a lógica da aplicação.

### Quarantine

Registros inválidos são preservados com seus respectivos erros, permitindo investigação posterior.

### Sem dependência de infraestrutura externa

O projeto pode ser executado localmente sem necessidade de:

* banco de dados;
* Docker;
* Airflow;
* Spark;
* cloud provider.

Isso mantém o projeto adequado ao objetivo de demonstrar os fundamentos da Engenharia de Dados sem adicionar componentes que não sejam necessários ao problema.

---

# Possíveis evoluções

O projeto foi construído de forma que possa evoluir para cenários mais próximos de produção.

Possíveis extensões incluem:

* persistência em banco de dados;
* camadas Bronze/Silver/Gold;
* particionamento por data e localização;
* controle de execução;
* métricas de Data Quality;
* observabilidade;
* CI/CD;
* execução em cloud;
* scheduler;
* orquestração com ferramentas especializadas;
* armazenamento em Data Lake;
* processamento incremental.

Essas evoluções não fazem parte do escopo atual porque aumentariam a complexidade sem serem necessárias para demonstrar o fluxo fundamental da pipeline.

---

# Objetivo de portfólio

Este projeto demonstra conhecimentos práticos em:

* Python para Engenharia de Dados;
* consumo de APIs;
* ingestão de dados;
* transformação;
* validação;
* Data Quality;
* tratamento de erros;
* retries;
* quarantine;
* persistência;
* orchestration;
* testes automatizados;
* configuração externa;
* execução operacional;
* logging;
* organização de projetos;
* Git e GitHub.

O foco não é apenas fazer a API funcionar, mas demonstrar como estruturar uma pequena pipeline de dados com responsabilidades bem definidas e possibilidade de evolução.

---

# Licença

Projeto desenvolvido para fins de estudo e portfólio.

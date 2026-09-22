# Open-Meteo Air Quality Pipeline

Pipeline de Data Engineering desenvolvido em Python para ingestão, transformação, validação e persistência de dados de qualidade do ar provenientes da API Open-Meteo.

O projeto foi construído com foco em boas práticas de engenharia de dados, separação de responsabilidades, tratamento de erros e testes automatizados.

## Arquitetura

```text
Open-Meteo API
      ↓
  API Client
      ↓
   Ingestion
      ↓
 Transformation
      ↓
 Orchestration
      ↓
   Validation
    ↙       ↘
Output    Quarantine
  ↓           ↓
JSONL        JSONL
```

### Fluxo

1. **API Client** — comunica com a API Open-Meteo e implementa mecanismos de retry para falhas transitórias.
2. **Ingestion** — obtém os dados para as localizações configuradas.
3. **Transformation** — transforma a resposta da API em registros estruturados.
4. **Validation** — verifica a qualidade dos registros.
5. **Orchestration** — encaminha cada registro para o fluxo correspondente.
6. **Output** — persiste registros válidos em JSONL.
7. **Quarantine** — armazena registros inválidos juntamente com os erros encontrados.

## Tecnologias

* Python 3.12
* pytest
* httpx
* YAML
* JSONL
* Git / GitHub

## Estrutura do projeto

```text
open-meteo-air-quality-pipeline/
│
├── config/
│   ├── locations.yaml
│   └── pipeline.yaml
│
├── data/
│   ├── processed/
│   └── raw/
│
├── logs/
│
├── src/
│   ├── api/
│   │   └── open_meteo.py
│   ├── ingestion/
│   │   └── air_quality.py
│   ├── orchestration/
│   │   └── air_quality.py
│   ├── output/
│   │   └── air_quality.py
│   ├── quarantine/
│   │   └── air_quality.py
│   ├── transformation/
│   │   └── air_quality.py
│   ├── validation/
│   │   └── air_quality.py
│   └── config.py
│
├── tests/
│   ├── test_config.py
│   ├── test_ingestion.py
│   ├── test_open_meteo.py
│   ├── test_orchestration.py
│   ├── test_output.py
│   ├── test_pipeline_integration.py
│   ├── test_quarantine.py
│   ├── test_transformation.py
│   └── test_validation.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Validação e qualidade dos dados

O pipeline valida os principais campos dos registros de qualidade do ar, incluindo:

* timestamp;
* latitude;
* longitude;
* PM10;
* PM2.5;
* monóxido de carbono.

Quando um registro é inválido, os erros encontrados são acumulados e o registro é encaminhado para a quarentena.

Exemplo:

```json
{
  "record": {
    "latitude": 999,
    "pm10": -5
  },
  "errors": [
    "Invalid latitude",
    "Invalid pm10"
  ]
}
```

## Testes

O projeto possui testes unitários para os principais componentes e testes de integração para validar o fluxo entre as diferentes camadas.

Execução da suíte completa:

```bash
python -m pytest
```

Estado atual:

```text
67 passed
```

## Princípios utilizados

O projeto procura manter responsabilidades separadas:

* comunicação com a API isolada no API Client;
* ingestão separada da transformação;
* validação independente da persistência;
* registros inválidos tratados através de uma quarentena;
* componentes testados isoladamente;
* integração validada sem depender da API real.

## Objetivo do projeto

Este projeto faz parte de um portfólio de Data Engineering e tem como objetivo demonstrar, através de um exemplo prático, conhecimentos em:

* consumo de APIs;
* pipelines de dados;
* transformação de dados;
* data quality;
* tratamento de erros;
* persistência de dados;
* testes automatizados;
* organização modular de projetos Python.

## Próximos passos

Possíveis evoluções futuras incluem:

* execução automatizada do pipeline;
* persistência em formatos analíticos, como Parquet;
* utilização de DuckDB;
* logging estruturado;
* CI/CD;
* agendamento de execuções.

Essas funcionalidades ficam fora do escopo atual da primeira versão.

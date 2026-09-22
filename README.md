# Desempenho-de-campanhas-de-marketing-Jan-2025-a-Jun-2025

Pipeline de dados desenvolvido para demonstrar um fluxo completo de **ingestão, exploração, limpeza, validação, transformação, análise e visualização de dados** com objetivo de aferir a efetividade de algumas campanhas de marketing feitas por uma empresa.

O projeto utiliza Python/Pandas e SQL para transformar uma base "suja" e propositalmente inconsistente em datasets confiáveis para análise de negócio e ferramentas de BI.

## Objetivo

Construir um pipeline capaz de transformar dados brutos de campanhas de marketing em informações estruturadas para responder perguntas como:

* Quais canais geram mais receita?
* Quais campanhas apresentam maior ROAS (retorno sobre investimento)?
* Quanto custa adquirir um cliente?
* Qual o custo por lead?
* Como o desempenho das campanhas evolui ao longo do tempo?
* Quais canais apresentam melhor conversão?
* Onde existem problemas de qualidade nos dados?

Além da análise de negócio, o projeto demonstra práticas de **Data Quality e arquitetura de dados em camadas**.

## Arquitetura

O projeto possui duas implementações principais.

### Pipeline Python

CSV RAW
   ↓
Exploração
   ↓
Padronização
   ↓
Limpeza
   ↓
Validação
   ↓
Transformações
   ↓
Dataset analítico
   ↓
Power BI
```

### Pipeline SQL / AWS

```text
S3 RAW
   ↓
STAGING
   ↓
SILVER
   ↓
GOLD
   ├── Performance por Canal
   ├── Performance por Campanha
   └── Performance Mensal
           ↓
      Power BI / QuickSight
```

Os dados das camadas anteriores não são sobrescritos. Cada etapa gera uma nova camada ou tabela, permitindo rastreabilidade e reprocessamento.

---

## Tecnologias

* Python
* Pandas
* NumPy
* SQL
* Amazon S3
* Amazon Athena
* AWS Glue
* PySpark
* Power BI
* Amazon QuickSight
* Git / GitHub

---

## Estrutura do projeto

```text
marketing-data-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_exploracao_dados.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analise_marketing.ipynb
│
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── validation/
│   └── transformations/
│
├── sql/
│   ├── 01_staging.sql
│   ├── 02_silver.sql
│   ├── 03_gold.sql
│   ├── 04_dashboard_queries.sql
│   └── 05_data_quality.sql
│
├── dashboard/
├── tests/
└── docs/
```

---

## Dados

A base utilizada no projeto é propositalmente "suja" para simular problemas encontrados em ambientes reais.

Entre os problemas presentes estão:

* valores nulos;
* categorias inconsistentes;
* diferenças de capitalização;
* erros de digitação;
* valores monetários em formatos diferentes;
* valores negativos;
* inconsistências no funil de conversão;
* registros duplicados;
* valores incompatíveis entre etapas do funil.

Exemplos de inconsistências:

```text
Brasil
brasil
BRA
BR
brazil
```

ou:

```text
Social
Social Media
socail
socia
```

O objetivo é utilizar essas inconsistências para demonstrar um processo realista de tratamento e validação.

---

## Camadas de dados

### Raw / Bronze

Contém os dados originais.

**Objetivo:** preservar a fonte sem alterações.

```text
marketing_raw
```

---

### Staging

Realiza preparações iniciais, principalmente tipagem e normalização básica.

```text
marketing_staging
```

---

### Silver

Contém os dados tratados e padronizados, mantendo a granularidade da origem.

```text
marketing_silver
```

Nesta camada são aplicadas regras como:

* padronização de categorias;
* tratamento de valores nulos;
* tratamento de valores negativos;
* validação das etapas do funil;
* remoção de duplicidades.

---

### Gold

Contém datasets agregados e preparados para consumo analítico.

```text
marketing_gold_channel
marketing_gold_campaign
marketing_gold_monthly
```

Cada tabela possui uma granularidade específica para facilitar o consumo por ferramentas de BI.

---

## Principais KPIs

### Aquisição

**CTR**

```text
Cliques / Impressões
```

**CPC**

```text
Investimento / Cliques
```

**CPL**

```text
Investimento / Leads
```

**CPQL**

```text
Investimento / Leads Qualificados
```

**CAC**

```text
Investimento / Clientes
```

### Conversão

**Lead Qualification Rate**

```text
Leads Qualificados / Leads
```

**Lead to Customer Rate**

```text
Clientes / Leads
```

### Receita

**ROAS**

```text
Receita / Investimento
```

**ROI**

```text
(Receita - Investimento) / Investimento
```

### E-mail

**Open Rate**

```text
E-mails Abertos / E-mails Enviados
```

**Email Click Rate**

```text
Cliques em E-mail / E-mails Enviados
```

**CTOR**

```text
Cliques em E-mail / E-mails Abertos
```

---

## Regra importante para os KPIs

Os indicadores agregados são calculados a partir dos valores totais.

Por exemplo:

```text
CTR = SUM(cliques) / SUM(impressoes)
```

em vez de:

```text
AVG(cliques / impressoes)
```

Isso evita distorções causadas por médias simples de indicadores calculados em diferentes níveis de granularidade.

---

## Data Quality

O projeto possui validações para regras de negócio como:

```text
Cliques <= Impressões

Leads Qualificados <= Leads

Clientes <= Leads Qualificados

E-mails Abertos <= E-mails Enviados

Cliques de E-mail <= E-mails Abertos
```

Também são monitorados:

* valores nulos;
* valores negativos;
* datas inválidas;
* categorias desconhecidas;
* duplicidades.

---

## Dashboard

O dashboard apresenta diferentes perspectivas da performance de marketing:

### Executive Overview

* investimento;
* receita;
* leads;
* clientes;
* CAC;
* ROAS;
* ROI.

### Performance por Canal

* investimento;
* receita;
* CTR;
* CPL;
* CAC;
* ROAS.

### Performance por Campanha

* campanha;
* canal;
* investimento;
* receita;
* leads;
* clientes;
* CAC;
* ROAS;
* ROI.

### Evolução Temporal

* investimento mensal;
* receita mensal;
* leads;
* clientes;
* CAC;
* ROAS.

---

## Execução do pipeline Python

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python -m src.pipeline
```

Os resultados são armazenados em:

```text
data/processed/
```

---

## SQL / AWS

A implementação SQL foi desenvolvida considerando uma arquitetura baseada em:

```text
Amazon S3
      ↓
Amazon Athena
      ↓
Staging
      ↓
Silver
      ↓
Gold
      ↓
Power BI / QuickSight
```

As tabelas são materializadas em cada etapa, preservando as camadas anteriores.

---

## Objetivo profissional

Este projeto foi desenvolvido como um projeto de portfólio para demonstrar conhecimentos em:

* análise exploratória de dados;
* Python;
* Pandas;
* SQL;
* Data Quality;
* modelagem de dados;
* criação de KPIs;
* AWS;
* processamento de dados;
* BI;
* construção de pipelines;
* organização de projetos de dados.

---

## Próximas evoluções

Possíveis evoluções do projeto:

* implementação completa em PySpark;
* execução do pipeline utilizando AWS Glue;
* orquestração com AWS Step Functions;
* criação de modelo dimensional;
* implementação de testes automatizados;
* CI/CD;
* monitoramento do pipeline;
* particionamento e otimização das tabelas no S3;
* utilização de formatos colunares como Parquet;
* camada semântica para Power BI/QuickSight.


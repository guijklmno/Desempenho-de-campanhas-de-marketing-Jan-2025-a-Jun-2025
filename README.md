# Desempenho-de-campanhas-de-marketing-Jan-2025-a-Jun-2025

Pipeline de dados desenvolvido para demonstrar um fluxo completo de **ingestão, exploração, limpeza, validação, transformação, análise e visualização de dados** com objetivo de aferir a efetividade de algumas campanhas de marketing feitas por uma empresa.

O projeto utiliza Python/Pandas e SQL para transformar uma base "suja" e propositalmente inconsistente em datasets confiáveis para análise de negócio e ferramentas de BI.

O projeto ainda está em andamento.
---

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


## Problema de Negócio

Uma empresa de marketing possui dados provenientes de diferentes campanhas, canais e plataformas, mas os dados brutos apresentam problemas de qualidade como valores inconsistentes, categorias duplicadas, registros duplicados, valores negativos, métricas incompatíveis com o funil de marketing e outliers.

Nesse cenário, simplesmente conectar a base a uma ferramenta de BI pode gerar indicadores incorretos e, consequentemente, decisões de negócio baseadas em informações pouco confiáveis.

O objetivo deste projeto é transformar uma base desorganizada em uma fonte de dados confiável e reutilizável para análises, permitindo que as áreas de Marketing e Business Intelligence respondam perguntas como:

- Quais campanhas geram mais receita?
- Quais canais apresentam melhor retorno sobre o investimento?
- Quanto custa adquirir um novo cliente?
- Quais campanhas possuem maior eficiência na geração de leads?
- Onde o orçamento de marketing está concentrado?
- Quais campanhas devem ser investigadas para otimização?
- Como os resultados evoluem ao longo do tempo?

### Por que Python e SQL?

O uso combinado de Python e SQL representa uma abordagem próxima de um cenário real.

**Python** é utilizado principalmente para:

- Exploração e profiling dos dados;
- Identificação de inconsistências;
- Padronização de categorias;
-  Tratamento de valores nulos e inválidos;
- Conversão e validação de tipos;
- Identificação de duplicidades e outliers;
- Aplicação de regras de Data Quality;
- Criação de transformações reutilizáveis e testáveis.

**SQL** é utilizado para estruturar o dado em diferentes camadas como um processo separado da ferramenta de visualização:

`Raw → Staging → Silver → Gold`

A camada **Gold** concentra datasets analíticos já agregados, permitindo que ferramentas como Power BI e QuickSight consumam desses dados para análise sem precisar reproduzir regras de limpeza e calcular métricas e indicadores em cada dashboard.

Essa separação também permite que as regras de negócio sejam centralizadas no pipeline.

---

## Resultados

Após o processo de tratamento e validação, a análise foi realizada sobre **652 registros válidos**, considerando a remoção de duplicidades exatas e o tratamento de registros identificados como outliers de investimento.

No período analisado, foram identificados aproximadamente:

| Indicador                 |            Resultado |
| ------------------------- | -------------------: |
| Investimento em marketing |  **R$ 2,16 milhões** |
| Receita atribuída         | **R$ 23,17 milhões** |
| ROAS                      |           **10,75x** |
| Clientes atribuídos       |         **~120 mil** |
| Impressões                |      **~37 milhões** |
| Cliques                   |      **~1,5 milhão** |

- **ROAS = Receita / Investimento**

Isso significa que, considerando os dados tratados, cada R$ 1,00 investido nas campanhas esteve associado a aproximadamente **R$ 10,75 em receita atribuída**.

### Desempenho por campanha

A análise das campanhas apresentou diferenças relevantes de eficiência:

| Campanha           | Investimento |    Receita |       ROAS |      CAC |
| ------------------ | -----------: | ---------: | ---------: | -------: |
| Instagram          |   R$ 222 mil | R$ 2,81 mi | **12,63x** | R$ 19,87 |
| Meta Ads           |   R$ 268 mil | R$ 3,23 mi | **12,05x** | R$ 20,10 |
| YouTube Ads        |   R$ 219 mil | R$ 2,60 mi | **11,84x** | R$ 20,90 |
| Email Black Friday |   R$ 277 mil | R$ 3,01 mi | **10,87x** | R$ 20,75 |
| Google Ads         |   R$ 371 mil | R$ 4,03 mi | **10,86x** | R$ 23,58 |
| Influenciadores    |   R$ 245 mil | R$ 2,57 mi | **10,46x** | R$ 20,63 |
| Remarketing        |   R$ 264 mil | R$ 2,41 mi |  **9,14x** | R$ 26,51 |
| Newsletter         |   R$ 287 mil | R$ 2,51 mi |  **8,72x** | R$ 25,24 |

### Principais Insights

**1. Social Media apresenta forte eficiência**

Social Media concentrou aproximadamente **22,8% do investimento**, mas foi responsável por cerca de **26,1% da receita**, apresentando ROAS de aproximadamente **12,31x**.

Isso indica uma relação favorável entre participação no orçamento e participação na receita, principalmente devido ao desempenho das campanhas de Instagram e Meta Ads.

**2. Instagram apresentou o maior ROAS entre as campanhas**

A campanha de Instagram apresentou aproximadamente **12,63x de ROAS**, com CAC de aproximadamente **R$ 19,87**.

Além do retorno elevado, a campanha gerou aproximadamente **11,2 mil clientes atribuídos**, indicando que o resultado não está baseado apenas em uma pequena quantidade de conversões.

**3. Google Ads possui grande contribuição em volume**

Google Ads apresentou aproximadamente **R$ 4,03 milhões em receita**, sendo a campanha com maior receita absoluta no período.

Seu ROAS de **10,86x** também demonstra eficiência, porém o CAC de aproximadamente **R$ 23,58** é superior ao observado em Instagram, Meta Ads e YouTube Ads.

**4. Newsletter e Remarketing merecem investigação**

Newsletter apresentou ROAS de aproximadamente **8,72x**, enquanto Remarketing apresentou **9,14x**.

Esses resultados continuam representando retorno positivo, mas ambas as campanhas apresentaram eficiência inferior às demais campanhas analisadas.

Newsletter, por exemplo, concentrou aproximadamente **13,3% do investimento**, mas respondeu por cerca de **10,8% da receita**.

Expandindo para um ambiente real, o comportamento desses dados pode indicar oportunidade para revisar segmentação, público, criativos, frequência de comunicação e estratégia de investimento.

**5. O processo de Data Quality impacta diretamente a análise**

A base original continha **670 registros** e apresentava:

* 16 registros duplicados;
* valores negativos em métricas;
* inconsistências entre etapas do funil;
* categorias com diferentes representações para o mesmo canal;
* registros com investimentos extremamente elevados;
* valores de e-mail incompatíveis com o volume enviado.

Sem o processo de tratamento, esses problemas poderiam distorcer indicadores como **ROAS, CAC, CTR e ROI**.

Um exemplo importante foram os registros com investimento próximo de **R$ 1 milhão**, muito acima do padrão observado nas demais linhas, que decidi retirar da análise. Caso fossem utilizados diretamente nos cálculos, alterariam significativamente a interpretação do desempenho de Newsletter e Meta Ads.

---

### Valor gerado pelo projeto

O principal resultado deste projeto é transformar uma pergunta de negócio:

> **"Onde estamos investindo nosso orçamento de marketing e quais campanhas estão gerando retorno?"**

em um processo analítico reproduzível:

`Dados Brutos → Data Quality → Dados Confiáveis → KPIs → Análise → Insight → Decisão de Negócio`

Esse fluxo demonstra como ferramentas de **Python, SQL, AWS e BI** podem ser utilizadas conjuntamente para transformar dados operacionais em informações utilizadas na tomada de decisão.



## Arquitetura

O projeto possui duas implementações principais.

### Pipeline Python

```text
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

### Pipeline SQL

```text
  RAW
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

- Python
- SQL
- Power BI


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
│   ├── eda.ipynb
│   ├── limpando_dados.ipynb
│   └── analise_campanhas.ipynb
│
├── src/
│   ├── ingestao/
│   ├── limpeza/
│   ├── validacao/
│   └── transformacao/
│
├── sql/
│   ├── staging.sql
│   ├── silver.sql
│   ├── gold.sql
│   ├── dashboard_queries.sql
│   └── data_quality.sql
│
├── dashboard/
├── tests/
└── docs/
```

---

## Dados

A base utilizada no projeto é propositalmente "suja" para simular problemas encontrados em ambientes reais.

Os problemas presentes são:

- valores nulos;
- colunas com valores categóricos inconsistentes;
- diferenças de capitalização;
- erros de digitação;
- valores monetários em formatos diferentes;
- valores negativos;
- inconsistências no funil de conversão;
- registros duplicados;
- valores incompatíveis entre etapas do funil.

Exemplos de inconsistências em campos de categoria:

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

O objetivo é utilizar essas inconsistências para demonstrar um processo de tratamento e validação.

---

## Camadas de dados

### Raw / Bronze

Contém os dados originais.

**Objetivo:** Ingestar os dados no fluxo preservando a fonte sem alterações.

```text
marketing_raw
```

---

### Staging

**Objetivo:** Realizar preparações iniciais, tipagem e normalização básica dos valores.

```text
marketing_staging
```

---

### Silver

**Objetivo:** Contém os dados tratados e padronizados, mantendo a granularidade da origem.

```text
marketing_silver
```

Nesta camada são aplicadas regras como:

- padronização de categorias;
- tratamento de valores nulos;
- tratamento de valores negativos;
- validação das etapas do funil;
- remoção de duplicidades.

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


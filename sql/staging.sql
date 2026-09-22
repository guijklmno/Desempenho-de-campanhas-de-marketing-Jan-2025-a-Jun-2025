-- ============================================================
-- Camada: STAGING
--
-- Objetivo:
--   Ler os dados do arquivo RAW e realizar somente a preparação inicial:
--   - Renomeação de colunas e conversão de tipos (cast)
--   - tratamento de strings vazias (trim)
--   - preservação da granularidade original
--
-- ============================================================

DROP TABLE IF EXISTS marketing_staging;

CREATE TABLE marketing_staging
WITH (
    format = 'PARQUET',
    external_location =
        's3://marketing-project/staging/marketing_staging/'
)
AS SELECT
    TRY_CAST(data AS DATE) AS data,
    TRIM(id_campanha) AS id_campanha,
    TRIM(campanha) AS campanha,
    LOWER(TRIM(canal)) AS canal,
    LOWER(TRIM(objetivo)) AS objetivo,
    LOWER(TRIM(plataforma)) AS plataforma,
    LOWER(TRIM(pais)) AS pais,
    LOWER(TRIM(regiao)) AS regiao,
    LOWER(TRIM(origem_trafego)) AS origem_trafego,
    TRY_CAST(impressoes AS BIGINT) AS impressoes,
    TRY_CAST(cliques AS BIGINT) AS cliques,
    TRY_CAST(investimento AS DOUBLE) AS investimento,
    TRY_CAST(receita AS DOUBLE) AS receita,
    TRY_CAST(leads AS BIGINT) AS leads,
    TRY_CAST(leads_qualificados AS BIGINT) AS leads_qualificados,
    TRY_CAST(clientes AS BIGINT) AS clientes,
    TRY_CAST(emails_enviados AS BIGINT) AS emails_enviados,
    TRY_CAST(emails_abertos AS BIGINT) AS emails_abertos,
    TRY_CAST(emails_cliques AS BIGINT) AS emails_cliques,
    LOWER(TRIM(dispositivo)) AS dispositivo,
    LOWER(TRIM(tipo_usuario)) AS tipo_usuario
FROM marketing_raw;
-- ============================================================
-- Camada: GOLD
-- Datasets com agregações e métricas calculadas.
-- Dataset sumarizado por canal.
-- ============================================================

DROP TABLE IF EXISTS marketing_gold_channel;

CREATE TABLE marketing_gold_channel
WITH (
    format = 'PARQUET',
    external_location =
        's3://marketing-project/gold/marketing_gold_channel/'
)
AS

SELECT

    canal,
    SUM(impressoes) AS impressoes,
    SUM(cliques) AS cliques,
    SUM(investimento) AS investimento,
    SUM(receita) AS receita,
    SUM(leads) AS leads,
    SUM(leads_qualificados) AS leads_qualificados,
    SUM(clientes) AS clientes,
    SUM(emails_enviados) AS emails_enviados,
    SUM(emails_abertos) AS emails_abertos,
    SUM(emails_cliques) AS emails_cliques,

    -- ==========================
    -- KPIs do MARKETING 
    -- ==========================

    CAST(SUM(cliques) AS DOUBLE)
        / NULLIF(SUM(impressoes), 0)
        AS ctr,

    SUM(investimento)
        / NULLIF(SUM(cliques), 0)
        AS cpc,

    SUM(investimento)
        / NULLIF(SUM(leads), 0)
        AS cpl,

    SUM(investimento)
        / NULLIF(SUM(leads_qualificados), 0)
        AS cpql,

    SUM(investimento)
        / NULLIF(SUM(clientes), 0)
        AS cac,

    CAST(SUM(leads_qualificados) AS DOUBLE)
        / NULLIF(SUM(leads), 0)
        AS lead_qualification_rate,

    CAST(SUM(clientes) AS DOUBLE)
        / NULLIF(SUM(leads), 0)
        AS lead_to_customer_rate,

    SUM(receita)
        / NULLIF(SUM(investimento), 0)
        AS roas,

    (
        SUM(receita) - SUM(investimento)
    )
    / NULLIF(SUM(investimento), 0)
        AS roi,

    CAST(SUM(emails_abertos) AS DOUBLE)
        / NULLIF(SUM(emails_enviados), 0)
        AS email_open_rate,

    CAST(SUM(emails_cliques) AS DOUBLE)
        / NULLIF(SUM(emails_enviados), 0)
        AS email_click_rate,

    CAST(SUM(emails_cliques) AS DOUBLE)
        / NULLIF(SUM(emails_abertos), 0)
        AS email_ctor

FROM marketing_silver
GROUP BY canal;

-- ============================================================
-- PERFORMANCE POR CAMPANHA
-- ============================================================

DROP TABLE IF EXISTS marketing_gold_campaign;

CREATE TABLE marketing_gold_campaign
WITH (
    format = 'PARQUET',
    external_location =
        's3://marketing-project/gold/marketing_gold_campaign/'
)
AS

SELECT
    id_campanha,
    campanha,
    canal,
    objetivo,
    plataforma,
    SUM(impressoes) AS impressoes,
    SUM(cliques) AS cliques,
    SUM(investimento) AS investimento,
    SUM(receita) AS receita,
    SUM(leads) AS leads,
    SUM(leads_qualificados) AS leads_qualificados,
    SUM(clientes) AS clientes,

    -- KPIs

    CAST(SUM(cliques) AS DOUBLE)
        / NULLIF(SUM(impressoes), 0)
        AS ctr,

    SUM(investimento)
        / NULLIF(SUM(cliques), 0)
        AS cpc,

    SUM(investimento)
        / NULLIF(SUM(leads), 0)
        AS cpl,

    SUM(investimento)
        / NULLIF(SUM(leads_qualificados), 0)
        AS cpql,

    SUM(investimento)
        / NULLIF(SUM(clientes), 0)
        AS cac,

    SUM(receita)
        / NULLIF(SUM(investimento), 0)
        AS roas,

    (
        SUM(receita) - SUM(investimento)
    )
    / NULLIF(SUM(investimento), 0)
        AS roi

FROM marketing_silver
GROUP BY
    id_campanha,
    campanha,
    canal,
    objetivo,
    plataforma;

-- ============================================================
-- PERFORMANCE MENSAL
-- ============================================================

DROP TABLE IF EXISTS marketing_gold_monthly;

CREATE TABLE marketing_gold_monthly
WITH (
    format = 'PARQUET',
    external_location =
        's3://marketing-project/gold/marketing_gold_monthly/'
)
AS

SELECT
    DATE_TRUNC(
        'month',
        data
    ) AS mes,
    SUM(impressoes) AS impressoes,
    SUM(cliques) AS cliques,
    SUM(investimento) AS investimento,
    SUM(receita) AS receita,
    SUM(leads) AS leads,
    SUM(leads_qualificados) AS leads_qualificados,
    SUM(clientes) AS clientes,

    CAST(SUM(cliques) AS DOUBLE)
        / NULLIF(SUM(impressoes), 0)
        AS ctr,

    SUM(investimento)
        / NULLIF(SUM(cliques), 0)
        AS cpc,

    SUM(investimento)
        / NULLIF(SUM(leads), 0)
        AS cpl,

    SUM(investimento)
        / NULLIF(SUM(clientes), 0)
        AS cac,

    SUM(receita)
        / NULLIF(SUM(investimento), 0)
        AS roas,

    (
        SUM(receita) - SUM(investimento)
    )
    / NULLIF(SUM(investimento), 0)
        AS roi

FROM marketing_silver
GROUP BY
    DATE_TRUNC('month', data);
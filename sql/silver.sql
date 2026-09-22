-- ============================================================
-- Camada: SILVER
--
-- Objetivo:
--   Criar uma versão limpa e padronizada dos dados.
--  - Padronizando colunas de categoria
--  - Arrumando números incorretos segundo regra de negócio, ex: leads qualificados sendo maior que leads geral
--  - Retirando duplicadas
--
-- Granularidade:
--   Mantida igual à origem.
--
-- Não realizar agregações nesta camada.
-- ============================================================

DROP TABLE IF EXISTS marketing_silver;

CREATE TABLE marketing_silver
WITH (
    format = 'PARQUET',
    external_location =
        's3://marketing-project/silver/marketing_silver/'
)
AS

WITH cat_padronizada AS (

    SELECT
        data,
        id_campanha,
        campanha,
        
        CASE
            WHEN canal = 'video'
                THEN 'Video'

            WHEN canal IN ('email', 'e-mail')
                THEN 'Email'

            WHEN canal = 'display'
                THEN 'Display'

            WHEN canal IN (
                'social',
                'social media',
                'socail',
                'socia'
            )
                THEN 'Social Media'

            WHEN canal = 'search'
                THEN 'Search'

            WHEN canal = 'influencer'
                THEN 'Influencer'

            ELSE 'Unknown'
        END AS canal,
        objetivo,
        plataforma,

        CASE
            WHEN pais IN (
                'brazil',
                'brasil',
                'bra',
                'br'
            )
                THEN 'Brasil'

            ELSE 'Unknown'
        END AS pais,

        CASE
            WHEN regiao = 'sudeste'
                THEN 'Sudeste'

            WHEN regiao = 'nordeste'
                THEN 'Nordeste'

            WHEN regiao = 'sul'
                THEN 'Sul'

            WHEN regiao = 'centro-oeste'
                THEN 'Centro-Oeste'

            ELSE 'Unknown'
        END AS regiao,
        origem_trafego,

        GREATEST(
            COALESCE(impressoes, 0),
            0
        ) AS impressoes,

        GREATEST(
            COALESCE(cliques, 0),
            0
        ) AS cliques,

        GREATEST(
            COALESCE(investimento, 0),
            0
        ) AS investimento,

        GREATEST(
            COALESCE(receita, 0),
            0
        ) AS receita,

        GREATEST(
            COALESCE(leads, 0),
            0
        ) AS leads,

        GREATEST(
            COALESCE(leads_qualificados, 0),
            0
        ) AS leads_qualificados,

        GREATEST(
            COALESCE(clientes, 0),
            0
        ) AS clientes,

        GREATEST(
            COALESCE(emails_enviados, 0),
            0
        ) AS emails_enviados,

        GREATEST(
            COALESCE(emails_abertos, 0),
            0
        ) AS emails_abertos,

        GREATEST(
            COALESCE(emails_cliques, 0),
            0
        ) AS emails_cliques,

        CASE
            WHEN dispositivo = 'mobile'
                THEN 'Mobile'

            WHEN dispositivo = 'desktop'
                THEN 'Desktop'

            WHEN dispositivo = 'tablet'
                THEN 'Tablet'

            ELSE 'Unknown'
        END AS dispositivo,

        CASE
            WHEN tipo_usuario = 'new'
                THEN 'New'

            WHEN tipo_usuario = 'returning'
                THEN 'Returning'

            ELSE 'Unknown'
        END AS tipo_usuario

    FROM marketing_staging
),

validacao_funil AS (

    SELECT
        *,
        LEAST(
            cliques,
            impressoes
        ) AS cliques_final,

        LEAST(
            leads_qualificados,
            leads
        ) AS leads_qualificados_final,

        LEAST(
            clientes,
            leads_qualificados
        ) AS clientes_final,

        LEAST(
            emails_abertos,
            emails_enviados
        ) AS emails_abertos_final,

        LEAST(
            emails_cliques,
            emails_abertos
        ) AS emails_cliques_final

    FROM cat_padronizada
),

retirando_duplicadas AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY
                data,
                id_campanha,
                campanha,
                canal,
                plataforma
            ORDER BY data
        ) AS rn

    FROM validacao_funil
)

SELECT
    data,
    id_campanha,
    campanha,
    canal,
    objetivo,
    plataforma,
    pais,
    regiao,
    origem_trafego,
    impressoes,
    cliques_final AS cliques,
    investimento,
    receita,
    leads,
    leads_qualificados_final AS leads_qualificados,
    clientes_final AS clientes,
    emails_enviados,
    emails_abertos_final AS emails_abertos,
    emails_cliques_final AS emails_cliques,
    dispositivo,
    tipo_usuario
FROM retirando_duplicadas
WHERE rn = 1;
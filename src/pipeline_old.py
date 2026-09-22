import pandas as pd
import numpy as np


# ============================================================
# 1. IMPORTAÇÃO DADOS
# ============================================================

arquivo_campanhas = r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\raw\marketing_dirty_dataset.csv"

df = pd.read_csv(arquivo_campanhas)

print(f"Linhas iniciais: {len(df):,}")
print(f"Colunas: {len(df.columns)}")



df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# ===========================================================================
# 2. PADRONIZAÇÃO COLUNAS CATEGÓRICAS (colunas com valores pré-determinados)
# ===========================================================================

colunas_categoricas = [
    "id_campanha",
    "campanha",
    "canal",
    "objetivo",
    "plataforma",
    "pais",
    "regiao",
    "origem_trafego",
    "dispositivo",
    "tipo_usuario"
]

for coluna in colunas_categoricas:

    df[coluna] = (
        df[coluna]
        .astype("string")
        .str.strip()
        .str.lower()
    )


# ============================================================
# 3. PADRONIZAÇÃO VALORES CATEGÓRICOS
# ============================================================

mapas = {

    "pais": {
        "brazil": "Brasil",
        "brasil": "Brasil",
        "bra": "Brasil",
        "br": "Brasil"
    },

    "canal": {
        "video": "Video",
        "email": "Email",
        "e-mail": "Email",
        "display": "Display",
        "social": "Social Media",
        "social media": "Social Media",
        "socail": "Social Media",
        "socia": "Social Media",
        "search": "Search",
        "influencer": "Influencer"
    },

    "regiao": {
        "sudeste": "Sudeste",
        "nordeste": "Nordeste",
        "sul": "Sul",
        "centro-oeste": "Centro-Oeste"
    },

    "dispositivo": {
        "mobile": "Mobile",
        "desktop": "Desktop",
        "tablet": "Tablet"
    },

    "tipo_usuario": {
        "new": "New",
        "returning": "Returning"
    }
}


for coluna, mapa in mapas.items():

    df[coluna] = df[coluna].replace(mapa)


# ============================================================
# 4. PADRONIZAÇÃO VALORES NULL OU DESCONHECIDOS
# ============================================================

# Valores vazios e strings que representam ausência de informação

valores_nulos = [
    "",
    " ",
    "null",
    "none",
    "nan",
    "n/a",
    "na",
    "unknown"
]

for coluna in colunas_categoricas:

    df[coluna] = (
        df[coluna]
        .replace(valores_nulos, pd.NA)
    )


# ============================================================
# 5. CONVERSÃO DA DATA
# ============================================================

df["data"] = pd.to_datetime(
    df["data"],
    format="%d/%m/%Y",
    errors="coerce"
)


# ============================================================
# 6. CONVERSÃO DAS COLUNAS NUMÉRICAS
# ============================================================

colunas_numericas = [
    "impressoes",
    "cliques",
    "investimento",
    "receita",
    "leads",
    "leads_qualificados",
    "clientes",
    "emails_enviados",
    "emails_abertos",
    "emails_cliques"
]


# ------------------------------------------------------------
# Tratamento especial para valores monetários
# ------------------------------------------------------------

for coluna in ["investimento", "receita"]:

    df[coluna] = (
        df[coluna]
        .astype("string")
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )


# ------------------------------------------------------------
# Demais colunas numéricas
# ------------------------------------------------------------

for coluna in [
    "impressoes",
    "cliques",
    "leads",
    "leads_qualificados",
    "clientes",
    "emails_enviados",
    "emails_abertos",
    "emails_cliques"
]:

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )


# ============================================================
# 7. DATA QUALITY FLAGS
# ============================================================
#
# IMPORTANTE:
# Fazemos as validações ANTES de corrigir os valores.
#
# Assim conseguimos saber quantos problemas existiam na origem.
# ============================================================

df["dq_cliques_maior_impressoes"] = (
    df["cliques"] > df["impressoes"]
)

df["dq_leads_qualificados_maior_leads"] = (
    df["leads_qualificados"] > df["leads"]
)

df["dq_clientes_maior_leads_qualificados"] = (
    df["clientes"] > df["leads_qualificados"]
)

df["dq_abertos_maior_enviados"] = (
    df["emails_abertos"] > df["emails_enviados"]
)

df["dq_cliques_email_maior_abertos"] = (
    df["emails_cliques"] > df["emails_abertos"]
)

df["dq_investimento_negativo"] = (
    df["investimento"] < 0
)

df["dq_receita_negativa"] = (
    df["receita"] < 0
)

df["dq_cliques_negativos"] = (
    df["cliques"] < 0
)

df["dq_data_invalida"] = (
    df["data"].isna()
)


# ============================================================
# 8. TRATAMENTO DOS VALORES NUMÉRICOS INVÁLIDOS
# ============================================================
#
# Depois de identificar os problemas, podemos corrigi-los.
#
# Valores negativos de métricas que não fazem sentido
# são transformados em zero.
# ============================================================

colunas_nao_negativas = [
    "impressoes",
    "cliques",
    "investimento",
    "receita",
    "leads",
    "leads_qualificados",
    "clientes",
    "emails_enviados",
    "emails_abertos",
    "emails_cliques"
]

for coluna in colunas_nao_negativas:

    df[coluna] = (
        df[coluna]
        .clip(lower=0)
    )


# ============================================================
# 9. CORREÇÃO DE RELACIONAMENTOS IMPOSSÍVEIS
# ============================================================
#
# Exemplo:
#
# 1.000 leads
# 1.500 leads qualificados
#
# Não faz sentido.
#
# Em vez de simplesmente deixar o dado inconsistente,
# podemos limitar a métrica à etapa anterior do funil.
# ============================================================

df["leads_qualificados"] = np.minimum(
    df["leads_qualificados"],
    df["leads"]
)

df["clientes"] = np.minimum(
    df["clientes"],
    df["leads_qualificados"]
)

df["cliques"] = np.minimum(
    df["cliques"],
    df["impressoes"]
)

df["emails_abertos"] = np.minimum(
    df["emails_abertos"],
    df["emails_enviados"]
)

df["emails_cliques"] = np.minimum(
    df["emails_cliques"],
    df["emails_abertos"]
)


# ============================================================
# 10. REMOÇÃO DE DUPLICIDADES
# ============================================================

duplicados = df.duplicated().sum()

print(f"Duplicidades encontradas: {duplicados:,}")

df = df.drop_duplicates().reset_index(drop=True)

print(f"Linhas após remoção: {len(df):,}")


# ============================================================
# 11. DIMENSÕES DE DATA
# ============================================================

df["ano"] = df["data"].dt.year

df["mes"] = df["data"].dt.month

df["mes_nome"] = df["data"].dt.month_name()

df["ano_mes"] = (
    df["data"]
    .dt.to_period("M")
    .astype("string")
)


# ============================================================
# 12. KPIs POR LINHA
# ============================================================

def safe_divide(numerador, denominador):

    return np.where(
        denominador > 0,
        numerador / denominador,
        0
    )


# ------------------------------------------------------------
# CTR
# ------------------------------------------------------------

df["ctr"] = safe_divide(
    df["cliques"],
    df["impressoes"]
)


# ------------------------------------------------------------
# CPC
# ------------------------------------------------------------

df["cpc"] = safe_divide(
    df["investimento"],
    df["cliques"]
)


# ------------------------------------------------------------
# CPL
# ------------------------------------------------------------

df["cpl"] = safe_divide(
    df["investimento"],
    df["leads"]
)


# ------------------------------------------------------------
# CPQL
# ------------------------------------------------------------

df["cpql"] = safe_divide(
    df["investimento"],
    df["leads_qualificados"]
)


# ------------------------------------------------------------
# CAC
# ------------------------------------------------------------

df["cac"] = safe_divide(
    df["investimento"],
    df["clientes"]
)


# ------------------------------------------------------------
# Taxa de conversão
# ------------------------------------------------------------

df["conversion_rate"] = safe_divide(
    df["clientes"],
    df["cliques"]
)


# ------------------------------------------------------------
# Taxa de qualificação
# ------------------------------------------------------------

df["lead_qualification_rate"] = safe_divide(
    df["leads_qualificados"],
    df["leads"]
)


# ------------------------------------------------------------
# ROAS
# ------------------------------------------------------------

df["roas"] = safe_divide(
    df["receita"],
    df["investimento"]
)


# ------------------------------------------------------------
# ROI
# ------------------------------------------------------------

df["roi"] = safe_divide(
    df["receita"] - df["investimento"],
    df["investimento"]
)


# ============================================================
# 13. KPIs DE E-MAIL MARKETING
# ============================================================

df["email_open_rate"] = safe_divide(
    df["emails_abertos"],
    df["emails_enviados"]
)

df["email_click_rate"] = safe_divide(
    df["emails_cliques"],
    df["emails_enviados"]
)

df["email_ctor"] = safe_divide(
    df["emails_cliques"],
    df["emails_abertos"]
)


# ============================================================
# 14. DATA QUALITY SCORE
# ============================================================

colunas_dq = [
    "dq_cliques_maior_impressoes",
    "dq_leads_qualificados_maior_leads",
    "dq_clientes_maior_leads_qualificados",
    "dq_abertos_maior_enviados",
    "dq_cliques_email_maior_abertos",
    "dq_investimento_negativo",
    "dq_receita_negativa",
    "dq_cliques_negativos",
    "dq_data_invalida"
]

df["dq_erro"] = (
    df[colunas_dq]
    .any(axis=1)
)

df["dq_status"] = np.where(
    df["dq_erro"],
    "REVISAR",
    "OK"
)


# ============================================================
# 15. DATASET FINAL PARA ANÁLISE
# ============================================================

colunas_fato = [
    "data",
    "ano",
    "mes",
    "mes_nome",
    "ano_mes",
    "id_campanha",
    "campanha",
    "canal",
    "objetivo",
    "plataforma",
    "pais",
    "regiao",
    "origem_trafego",
    "dispositivo",
    "tipo_usuario",

    "impressoes",
    "cliques",
    "investimento",
    "receita",
    "leads",
    "leads_qualificados",
    "clientes",

    "emails_enviados",
    "emails_abertos",
    "emails_cliques",

    "ctr",
    "cpc",
    "cpl",
    "cpql",
    "cac",
    "conversion_rate",
    "lead_qualification_rate",
    "roas",
    "roi",

    "email_open_rate",
    "email_click_rate",
    "email_ctor",

    "dq_status"
]

df_fato = df[colunas_fato].copy()


# ============================================================
# 16. DATASET AGREGADO PARA DASHBOARD
# ============================================================
#
# Aqui estamos criando a camada GOLD.
#
# O Power BI não precisa necessariamente trabalhar
# diretamente sobre os registros transacionais.
# ============================================================

df_dashboard = (
    df_fato
    .groupby(
        [
            "ano_mes",
            "canal"
        ],
        as_index=False
    )
    .agg({

        "impressoes": "sum",
        "cliques": "sum",
        "investimento": "sum",
        "receita": "sum",
        "leads": "sum",
        "leads_qualificados": "sum",
        "clientes": "sum",

        "emails_enviados": "sum",
        "emails_abertos": "sum",
        "emails_cliques": "sum"

    })
)


# ============================================================
# 17. KPIs AGREGADOS
# ============================================================
#
# ATENÇÃO:
# Não fazemos média simples de CTR, CPC, ROAS etc.
#
# Recalculamos os indicadores a partir dos totais.
# ============================================================

df_dashboard["ctr"] = safe_divide(
    df_dashboard["cliques"],
    df_dashboard["impressoes"]
)

df_dashboard["cpc"] = safe_divide(
    df_dashboard["investimento"],
    df_dashboard["cliques"]
)

df_dashboard["cpl"] = safe_divide(
    df_dashboard["investimento"],
    df_dashboard["leads"]
)

df_dashboard["cpql"] = safe_divide(
    df_dashboard["investimento"],
    df_dashboard["leads_qualificados"]
)

df_dashboard["cac"] = safe_divide(
    df_dashboard["investimento"],
    df_dashboard["clientes"]
)

df_dashboard["conversion_rate"] = safe_divide(
    df_dashboard["clientes"],
    df_dashboard["cliques"]
)

df_dashboard["lead_qualification_rate"] = safe_divide(
    df_dashboard["leads_qualificados"],
    df_dashboard["leads"]
)

df_dashboard["roas"] = safe_divide(
    df_dashboard["receita"],
    df_dashboard["investimento"]
)

df_dashboard["roi"] = safe_divide(
    df_dashboard["receita"] - df_dashboard["investimento"],
    df_dashboard["investimento"]
)

df_dashboard["email_open_rate"] = safe_divide(
    df_dashboard["emails_abertos"],
    df_dashboard["emails_enviados"]
)

df_dashboard["email_click_rate"] = safe_divide(
    df_dashboard["emails_cliques"],
    df_dashboard["emails_enviados"]
)

df_dashboard["email_ctor"] = safe_divide(
    df_dashboard["emails_cliques"],
    df_dashboard["emails_abertos"]
)


# ============================================================
# 18. PERFORMANCE POR CAMPANHA
# ============================================================

df_campanhas_kpi = (
    df_fato
    .groupby(
        [
            "id_campanha",
            "campanha",
            "canal",
            "objetivo",
            "plataforma"
        ],
        as_index=False
    )
    .agg({

        "impressoes": "sum",
        "cliques": "sum",
        "investimento": "sum",
        "receita": "sum",
        "leads": "sum",
        "leads_qualificados": "sum",
        "clientes": "sum",
        "emails_enviados": "sum",
        "emails_abertos": "sum",
        "emails_cliques": "sum"

    })
)


# ============================================================
# 19. KPIs POR CAMPANHA
# ============================================================

df_campanhas_kpi["ctr"] = safe_divide(
    df_campanhas_kpi["cliques"],
    df_campanhas_kpi["impressoes"]
)

df_campanhas_kpi["cpc"] = safe_divide(
    df_campanhas_kpi["investimento"],
    df_campanhas_kpi["cliques"]
)

df_campanhas_kpi["cpl"] = safe_divide(
    df_campanhas_kpi["investimento"],
    df_campanhas_kpi["leads"]
)

df_campanhas_kpi["cpql"] = safe_divide(
    df_campanhas_kpi["investimento"],
    df_campanhas_kpi["leads_qualificados"]
)

df_campanhas_kpi["cac"] = safe_divide(
    df_campanhas_kpi["investimento"],
    df_campanhas_kpi["clientes"]
)

df_campanhas_kpi["roas"] = safe_divide(
    df_campanhas_kpi["receita"],
    df_campanhas_kpi["investimento"]
)

df_campanhas_kpi["roi"] = safe_divide(
    df_campanhas_kpi["receita"] -
    df_campanhas_kpi["investimento"],
    df_campanhas_kpi["investimento"]
)

df_campanhas_kpi["conversion_rate"] = safe_divide(
    df_campanhas_kpi["clientes"],
    df_campanhas_kpi["cliques"]
)

df_campanhas_kpi["lead_qualification_rate"] = safe_divide(
    df_campanhas_kpi["leads_qualificados"],
    df_campanhas_kpi["leads"]
)


# ============================================================
# 20. RANKING DE CAMPANHAS
# ============================================================

df_campanhas_kpi["rank_roas"] = (
    df_campanhas_kpi["roas"]
    .rank(
        ascending=False,
        method="dense"
    )
)

df_campanhas_kpi["rank_receita"] = (
    df_campanhas_kpi["receita"]
    .rank(
        ascending=False,
        method="dense"
    )
)


# ============================================================
# 21. VISÃO EXECUTIVA
# ============================================================

total_investimento = df_fato["investimento"].sum()

total_receita = df_fato["receita"].sum()

total_impressoes = df_fato["impressoes"].sum()

total_cliques = df_fato["cliques"].sum()

total_leads = df_fato["leads"].sum()

total_leads_qualificados = (
    df_fato["leads_qualificados"].sum()
)

total_clientes = df_fato["clientes"].sum()


dashboard_executivo = pd.DataFrame({

    "KPI": [

        "Investimento",
        "Receita",
        "ROAS",
        "ROI",
        "Impressões",
        "Cliques",
        "CTR",
        "Leads",
        "Leads Qualificados",
        "Taxa de Qualificação",
        "Clientes",
        "CAC",
        "CPC",
        "CPL",
        "CPQL",
        "Conversion Rate"

    ],

    "Valor": [

        total_investimento,

        total_receita,

        total_receita / total_investimento
        if total_investimento > 0 else 0,

        (
            (total_receita - total_investimento)
            / total_investimento
        )
        if total_investimento > 0 else 0,

        total_impressoes,

        total_cliques,

        total_cliques / total_impressoes
        if total_impressoes > 0 else 0,

        total_leads,

        total_leads_qualificados,

        total_leads_qualificados / total_leads
        if total_leads > 0 else 0,

        total_clientes,

        total_investimento / total_clientes
        if total_clientes > 0 else 0,

        total_investimento / total_cliques
        if total_cliques > 0 else 0,

        total_investimento / total_leads
        if total_leads > 0 else 0,

        total_investimento / total_leads_qualificados
        if total_leads_qualificados > 0 else 0,

        total_clientes / total_cliques
        if total_cliques > 0 else 0

    ]
})


# ============================================================
# 22. EXPORTAÇÃO
# ============================================================

df_fato.to_csv(
    r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\processed\marketing_fato.csv",
    index=False
)

df_dashboard.to_csv(
    r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\processed\marketing_dashboard.csv",
    index=False
)

df_campanhas_kpi.to_csv(
    r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\processed\marketing_campanhas_kpi.csv",
    index=False
)

dashboard_executivo.to_csv(
    r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\processed\marketing_executivo.csv",
    index=False
)


# ============================================================
# 23. RESUMO FINAL
# ============================================================

print("\n" + "=" * 60)
print("PIPELINE FINALIZADO")
print("=" * 60)

print(f"Linhas finais: {len(df_fato):,}")

print(
    f"Registros com problemas de qualidade: "
    f"{(df_fato['dq_status'] == 'REVISAR').sum():,}"
)

print("\nKPIs EXECUTIVOS:")
print(dashboard_executivo.to_string(index=False))


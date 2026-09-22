import numpy as np
import pandas as pd

#impedindo divisao por 0

def safe_divide(numerador, denominador):

    return np.where(
        denominador > 0,
        numerador / denominador,
        0
    )


def add_date_dimension(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["ano"] = df["data"].dt.year

    df["mes"] = df["data"].dt.month

    df["mes_nome"] = (
        df["data"]
        .dt.month_name()
    )

    df["ano_mes"] = (
        df["data"]
        .dt.to_period("M")
        .astype("string")
    )

    return df


def calcular_metricas(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["ctr"] = safe_divide(
        df["cliques"],
        df["impressoes"]
    )

    df["cpc"] = safe_divide(
        df["investimento"],
        df["cliques"]
    )

    df["cpl"] = safe_divide(
        df["investimento"],
        df["leads"]
    )

    df["cpql"] = safe_divide(
        df["investimento"],
        df["leads_qualificados"]
    )

    df["cac"] = safe_divide(
        df["investimento"],
        df["clientes"]
    )

    df["conversion_rate"] = safe_divide(
        df["clientes"],
        df["cliques"]
    )

    df["lead_qualification_rate"] = safe_divide(
        df["leads_qualificados"],
        df["leads"]
    )

    df["roas"] = safe_divide(
        df["receita"],
        df["investimento"]
    )

    df["roi"] = safe_divide(
        df["receita"] - df["investimento"],
        df["investimento"]
    )

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

    return df


def sumarizar_por_canal(df: pd.DataFrame) -> pd.DataFrame:

    dimensoes = [
        "ano_mes",
        "canal"
    ]

    metricas = [
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

    df_sumarizado = (
        df
        .groupby(
            dimensoes,
            as_index=False
        )[metricas]
        .sum()
    )

    return calcular_metricas(df_sumarizado)


def sumarizar_por_campanha(df: pd.DataFrame) -> pd.DataFrame:

    dimensoes = [
        "id_campanha",
        "campanha",
        "canal",
        "objetivo",
        "plataforma"
    ]

    metricas = [
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

    df_sumarizado = (
        df
        .groupby(
            dimensoes,
            as_index=False
        )[metricas]
        .sum()
    )

    return calcular_metricas(df_sumarizado)
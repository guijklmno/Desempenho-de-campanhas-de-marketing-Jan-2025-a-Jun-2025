import numpy as np
import pandas as pd


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


colunas_monetarias = [
    "investimento",
    "receita"
]


def formatar_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["data"] = pd.to_datetime(
        df["data"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    return df


def limpar_colunas_monetarias(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for coluna in colunas_monetarias:

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

    return df


def limpar_colunas_numericas(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for coluna in colunas_numericas:

        if coluna in colunas_monetarias:
            continue

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    return df


def remover_duplicidades(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    return (
        df
        .drop_duplicates()
        .reset_index(drop=True)
    )


def identificar_valores_negativos(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for coluna in colunas_numericas:

        df[coluna] = (
            df[coluna]
            .clip(lower=0)
        )

    return df


def ajustar_linhas_numericas_inconsistentes(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["cliques"] = np.minimum(
        df["cliques"],
        df["impressoes"]
    )

    df["leads_qualificados"] = np.minimum(
        df["leads_qualificados"],
        df["leads"]
    )

    df["clientes"] = np.minimum(
        df["clientes"],
        df["leads_qualificados"]
    )

    df["emails_abertos"] = np.minimum(
        df["emails_abertos"],
        df["emails_enviados"]
    )

    df["emails_cliques"] = np.minimum(
        df["emails_cliques"],
        df["emails_abertos"]
    )

    return df


def limpar_dataframe(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = formatar_data(df)

    df = limpar_colunas_monetarias(df)

    df = limpar_colunas_numericas(df)

    df = identificar_valores_negativos(df)

    df = ajustar_linhas_numericas_inconsistentes(df)

    df = remover_duplicidades(df)

    return df
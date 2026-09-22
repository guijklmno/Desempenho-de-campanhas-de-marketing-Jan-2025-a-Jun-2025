import pandas as pd


def cria_df_linhas_inconsistentes(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["dq_cliques_maior_impressoes"] = (
        df["cliques"] > df["impressoes"]
    )

    df["dq_leads_quali_maior_leads"] = (
        df["leads_qualificados"] > df["leads"]
    )

    df["dq_clientes_maior_leads_quali"] = (
        df["clientes"] > df["leads_qualificados"]
    )

    df["dq_abertos_maior_enviados"] = (
        df["emails_abertos"] >
        df["emails_enviados"]
    )

    df["dq_cliques_email_maior_abertos"] = (
        df["emails_cliques"] >
        df["emails_abertos"]
    )

    df["dq_investimento_negativo"] = (
        df["investimento"] < 0
    )

    df["dq_receita_negativa"] = (
        df["receita"] < 0
    )

    df["dq_data_invalida"] = (
        df["data"].isna()
    )

    return df


def status_qualidade(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    dq_colunas = [
        colunas
        for coluna in df.columns
        if coluna.startswith("dq_")
    ]

    df["dq_erro"] = (
        df[dq_colunas]
        .any(axis=1)
    )

    df["dq_status"] = (
        df["dq_erro"]
        .map({
            True: "REVISAR",
            False: "OK"
        })
    )

    return df


def criar_report_data_quality(df: pd.DataFrame) -> pd.DataFrame:

    dq_colunas = [
        colunas
        for coluna in df.colunas
        if coluna.startswith("dq_")
        and coluna != "dq_erro"
        and coluna != "dq_status"
    ]

    report = []

    total_linhas = len(df)

    for coluna in dq_colunas:

        erros = int(df[coluna].sum())

        report.append({
            "regra": coluna,
            "erros": erros,
            "percentual_erro": (
                erros / total_linhas
                if total_linhas > 0
                else 0
            )
        })

    return pd.DataFrame(report)


def validar_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    df = cria_df_linhas_inconsistentes(df)

    df = status_qualidade(df)

    report = criar_report_data_quality(df)

    return df, report


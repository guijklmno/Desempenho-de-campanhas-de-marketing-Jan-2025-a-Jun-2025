import pandas as pd


valores_padrao_categorias = {

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


colunas_de_categoria = [
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


def padroniza_valores_em_colunas(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def padroniza_categorias(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for coluna in colunas_de_categoria:

        if coluna not in df.columns:
            continue

        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    return df


def aplica_valores_padrao_categorias(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for coluna, valor in valores_padrao_categorias.items():

        if coluna in df.columns:
            df[coluna] = df[coluna].replace(valor)

    return df


def trata_null_categorias(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    valores_vazios = [
        "",
        " ",
        "null",
        "none",
        "nan",
        "n/a",
        "na",
        "unknown"
    ]

    for coluna in colunas_de_categoria:

        if coluna not in df.columns:
            continue

        df[coluna] = (
            df[coluna]
            .replace(valores_vazios, pd.NA)
        )

    return df


def padroniza_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df = padroniza_valores_em_colunas(df)

    df = padroniza_categorias(df)

    df = aplica_valores_padrao_categorias(df)

    df = trata_null_categorias(df)

    return df
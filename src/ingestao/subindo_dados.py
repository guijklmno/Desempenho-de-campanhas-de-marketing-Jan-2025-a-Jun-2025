from pathlib import Path
import pandas as pd


"""
    Carrega um arquivo CSV em um DataFrame.

    Parameters
    ----------
    file_path : str
        Caminho do arquivo CSV.

    Returns
    -------
    pd.DataFrame
        Dados carregados.

    Raises
    ------
    FileNotFoundError
        Caso o arquivo não exista.
    """

# arquivo_campanhas = r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\raw\marketing_dirty_dataset.csv"

def ler_arquivo(path_arquivo: str) -> pd.DataFrame:
    path = Path(path_arquivo)

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path_arquivo}"
        )

    df = pd.read_csv(
        path,
        encoding="utf-8-sig"
    )
    return df


# df_campanhas = ler_arquivo(arquivo_campanhas)

# df_campanhas.to_csv(
#     r"C:\Users\x\Documents\Projetos Github\pipeline marketing\data\bronze\marketing_bronze.csv",
#     index=False
# )
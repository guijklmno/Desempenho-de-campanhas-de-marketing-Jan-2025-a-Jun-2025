from pathlib import Path

from ingestao.subindo_dados import ler_arquivo

from limpeza.padronizacao_dataset import (
    padroniza_dataframe
)

from limpeza.limpando_dados import (
    limpar_dataframe
)

from validacao.report_data_quality import (
    validar_dataframe
)

from transformacao.calculo_metricas import (
    add_date_dimension,
    calcular_metricas,
    sumarizar_por_canal,
    sumarizar_por_campanha
)


raw_path = (
    "data/raw/marketing_dirty_dataset.csv"
)

processed_path = Path(
    "data/processed"
)


def run_pipeline():

    print("=" * 60)
    print("MARKETING DATA PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. INGESTÃO
    # --------------------------------------------------------

    print("\n[1/6] Carregando dados...")

    df = ler_arquivo(raw_path)

    print(
        f"Registros carregados: {len(df):,}"
    )

    # --------------------------------------------------------
    # 2. STANDARDIZATION
    # --------------------------------------------------------

    print("\n[2/6] Padronizando dados...")

    df = padroniza_dataframe(df)

    # --------------------------------------------------------
    # 3. CLEANING
    # --------------------------------------------------------

    print("\n[3/6] Limpando dados...")

    df = limpar_dataframe(df)

    # --------------------------------------------------------
    # 4. DATA QUALITY
    # --------------------------------------------------------

    print("\n[4/6] Executando Data Quality...")

    df, quality_report = validar_dataframe(df)

    # --------------------------------------------------------
    # 5. TRANSFORMATIONS
    # --------------------------------------------------------

    print("\n[5/6] Calculando métricas...")

    df = add_date_dimension(df)

    df = calcular_metricas(df)

    dashboard = sumarizar_por_canal(df)

    campanhas = sumarizar_por_campanha(df)

    # --------------------------------------------------------
    # 6. EXPORT
    # --------------------------------------------------------

    print("\n[6/6] Exportando dados...")

    processed_path.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        processed_path / "marketing_fato.csv",
        index=False
    )

    dashboard.to_csv(
        processed_path / "marketing_dashboard.csv",
        index=False
    )

    campanhas.to_csv(
        processed_path / "marketing_campanhas_kpi.csv",
        index=False
    )

    quality_report.to_csv(
        processed_path / "data_quality_report.csv",
        index=False
    )

    print("\nPipeline concluído!")

    print(
        f"Fato: {len(df):,} registros"
    )

    print(
        f"Registros para revisão: "
        f"{(df['dq_status'] == 'REVISAR').sum():,}"
    )


if __name__ == "__main__":
    run_pipeline()
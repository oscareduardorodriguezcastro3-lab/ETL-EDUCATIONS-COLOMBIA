"""ETL educativo: conectividad fija, hogares y resultados Saber 11."""

__version__ = "1.1.0"

from .dataframes import cargar_dataframes, ejecutar_etl

__all__ = ["cargar_dataframes", "ejecutar_etl"]

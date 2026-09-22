"""Interfaz: python -m etl_medallon --config config/local.json [--inventory]."""

import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import sys
from uuid import uuid4

from . import __version__, bronze, silver, gold
from .common import save_json


def main():
    """Coordina las capas; solo publica latest.json al finalizar correctamente."""
    parser = argparse.ArgumentParser(description="ETL Medallón: Saber 11 e Internet fijo")
    parser.add_argument("--config", default="config/local.json")
    parser.add_argument("--inventory", action="store_true", help="Lista entradas sin procesarlas")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    source = Path(config["source_dir"]).expanduser().resolve()
    output = Path(config["output_dir"]).expanduser().resolve()
    years = config["years"]
    if (not years or any(type(y) is not int or not 2000 <= y <= 2100 for y in years)
            or len(set(years)) != len(years) or type(config["chunksize"]) is not int
            or config["chunksize"] <= 0):
        raise ValueError("Revise years (años únicos) y chunksize (entero positivo).")
    if args.inventory:
        for kind, paths in bronze.discover(source).items():
            for path in paths:
                print(f"{kind:5} | {path.stat().st_size:>12,} bytes | {path.name}")
        return
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid4().hex[:8]
    run = output / "runs" / run_id
    run.mkdir(parents=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(run / "pipeline.log", encoding="utf-8")])
    report = {"run_id": run_id, "version": __version__, "config": config, "status": "running"}
    save_json(run / "report.json", report)
    try:
        files = bronze.ingest(source, output, run)
        exam, internet, households, quality = silver.build(files, config, run)
        report.update(quality)
        report.update(gold.build(exam, internet, households, run))
        expected = {f"{year}{period}" for year in years for period in (1, 2)}
        report["periodos_icfes_faltantes"] = sorted(expected - set(quality["periodos_icfes"]))
        report["status"] = "completed"
        save_json(run / "report.json", report)
        # El puntero cambia al final: un fallo no sustituye una ejecución válida.
        pointer = output / f"latest.{run_id}.tmp"
        save_json(pointer, {"run_id": run_id, "path": str(run)})
        pointer.replace(output / "latest.json")
        logging.info("Terminado | %s", json.dumps(report, ensure_ascii=False))
    except Exception as error:
        report.update(status="failed", error=str(error))
        save_json(run / "report.json", report)
        logging.exception("Ejecución fallida; revise report.json y pipeline.log")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

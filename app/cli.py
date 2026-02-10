from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from app.config import DEFAULT_CONFIG_PATH, load_points
from app.service import WeatherModelService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Application de collecte de sorties modèles météo")
    parser.add_argument("command", choices=["refresh", "show", "run-scheduler"])
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Chemin du fichier de points")
    parser.add_argument("--storage", default="data/latest_forecasts.json", help="Fichier de stockage JSON")
    parser.add_argument(
        "--interval-hours",
        type=int,
        default=6,
        help="Intervalle d'actualisation en heures (commande run-scheduler)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    points = load_points(Path(args.config))
    service = WeatherModelService(points=points, storage_path=Path(args.storage))

    if args.command == "refresh":
        result = service.refresh_all()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.command == "show":
        result = service.get_latest()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.command == "run-scheduler":
        while True:
            result = service.refresh_all()
            print(f"[{result['updated_at']}] Rafraîchissement terminé pour {len(result['results'])} points")
            time.sleep(max(1, args.interval_hours) * 3600)


if __name__ == "__main__":
    main()

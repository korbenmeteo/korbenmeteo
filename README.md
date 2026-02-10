# korbenmeteo - Collecte de sorties modèles météo

Cette application Python récupère des sorties modèles météo pour une liste de points d'intérêt (villes), avec une logique de priorisation:

- **Londres / UK**: modèles haute résolution en priorité.
- **Villes US**: modèles haute résolution US en priorité.
- **Autres zones**: fallback sur des modèles globaux à maille plus large.

Les données sont récupérées via l'API Open-Meteo, stockées en JSON, et peuvent être mises à jour quelques fois par jour.

## Structure

- `config/points.json`: liste des points d'intérêt.
- `app/model_selection.py`: logique de sélection des modèles (HR puis fallback global).
- `app/service.py`: récupération des données et fallback par modèle.
- `app/cli.py`: commandes de mise à jour / affichage / scheduler.
- `data/latest_forecasts.json`: cache local des dernières sorties.

## Pré-requis

- Python 3.10+
- `pytest` (optionnel, pour les tests)

## Utilisation

### 1) Rafraîchir maintenant

```bash
python -m app.cli refresh
```

### 2) Voir le dernier cache

```bash
python -m app.cli show
```

### 3) Lancer une mise à jour périodique (ex: toutes les 6h)

```bash
python -m app.cli run-scheduler --interval-hours 6
```

## Personnaliser les villes

Modifiez `config/points.json` pour ajouter/supprimer des points.

## Tests

```bash
pytest -q
```

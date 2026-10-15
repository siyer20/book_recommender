**What each folder is for:**

| Folder | Purpose |
|--------|---------|
| `config/` | `config.yaml` — subjects, thresholds, weights, paths. Single source of truth for tunable behavior. |
| `data/raw/` | Raw API responses (`seeds.json`, `enriched.jsonl`). Large, regenerable, gitignored. |
| `data/processed/` | Cleaned datasets (`books_v1.parquet`). Versioned, gitignored except samples. |
| `data/artifacts/` | Derived artifacts (`similarity_v1.npz`, `feature_pipeline_v1.joblib`). Produced in Phase 2. |
| `evaluation/` | Evaluation results (`results_v1.json`). Produced in Phase 3. |
| `logs/` | Pipeline logs and run records. `logs/runs/` holds one JSON per pipeline execution. |
| `notebooks/` | Exploration and the Phase 3.5 demo notebook. |
| `src/` | All pipeline code. Importable as a module so `python -m src.pipeline` works. |
| `tests/` | pytest tests. |
| `api/` | FastAPI service (Phase 4). |
| `app/` | Streamlit UI (Phase 5). |
| `docs/` | Architecture docs, schema docs, evaluation writeups (Phase 7). |
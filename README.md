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


**Why `data/raw/` is fully ignored but `data/processed/` has exceptions:** raw data is fully regenerable and never useful to commit. Processed data is also regenerable, but you may want to commit a small sample (`books_sample.csv`) for reference and for testing in CI. The `.gitkeep` files keep the empty directories present in git.

**Why `evaluation/*.json` is ignored:** evaluation results are reproducible from a fixed dataset and config. Committing them creates noise. The evaluation report (Phase 7) will summarize them in a Markdown file that *is* committed.
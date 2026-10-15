# Book Recommender

A content-based book recommender. Users build a shelf of books they've read; the system returns ranked recommendations with explanations, based on a similarity matrix across author, genre, mood, length, era, and description.

**Status:** Phase 1 (data foundation) in progress.

## Architecture

See `docs/architecture.md` (to be written in Phase 7).

## Setup

### Prerequisites

- **Miniconda** (not full Anaconda) — https://docs.conda.io/en/latest/miniconda.html
- **Git**
- A **Google Books API key** — get one free at https://console.cloud.google.com/ (enable the Books API, then create an API key)

### Installation

The setup installs two categories of packages separately:

- **Compiled packages** (`pyarrow`, `rapidfuzz`) — installed via conda, because they contain native binaries that pip cannot reliably build from source.
- **Pure-Python packages** — installed via `uv pip` from `requirements.txt`, which is fast and clean.

The order matters. Install conda packages first, then pip packages.

```bash
# Clone and enter the repository
git clone <your-repo-url>
cd book-rec

# Create and activate the conda environment
conda create -n book-rec python=3.11 -y
conda activate book-rec

# Install the compiled dependencies via conda FIRST
conda install -c conda-forge pyarrow rapidfuzz -y

# Install uv, then the pure-Python dependencies
pip install uv
uv pip install -r requirements.txt

# Copy the environment file and add your Google Books API key
cp .env.example .env
# Then edit .env and set GOOGLE_BOOKS_API_KEY

# Run the data pipeline (Phase 1)
python -m src.pipeline
```

**Why conda for `pyarrow` and `rapidfuzz`:** both have compiled C/C++/Rust components. If `uv pip` cannot find a compatible prebuilt wheel for your platform, it falls back to a source build and requires a full compiler toolchain. Conda-forge provides prebuilt binaries that avoid this entirely.

**Why `uv pip` for the rest:** the remaining packages are pure Python. `uv pip` resolves and installs them 10–100× faster than plain `pip`, with identical results.

## Pipeline

Three stages, orchestrated by `python -m src.pipeline`:

1. **Seeds** (`src/build_seeds.py`) — fetch book metadata from Open Library.
2. **Enrich** (`src/enrich_google.py`) — fill missing fields from Google Books.
3. **Clean** (`src/clean.py`) — deduplicate, normalize, and produce `data/processed/books_v1.parquet`.

### Incremental updates

To fetch only books that aren't already in the dataset (added in Phase 1, used by the Level 2 update workflow):

```bash
python -m src.pipeline --incremental
```

## Repository Structure

```text
book-rec/
├── config/          # config.yaml — all tunable behavior
├── data/
│   ├── raw/         # API responses (gitignored)
│   ├── processed/   # books_v1.parquet (gitignored except samples)
│   └── artifacts/   # similarity matrices, fitted pipelines (Phase 2+)
├── evaluation/      # evaluation results (Phase 3+)
├── logs/            # pipeline logs and run records
├── notebooks/       # exploration and demo
├── src/             # pipeline code
├── tests/           # pytest tests
├── api/             # FastAPI service (Phase 4+)
├── app/             # Streamlit UI (Phase 5+)
└── docs/            # architecture and schema documentation (Phase 7+)
```

## Package Management Rules

This project uses two package managers with a clear boundary:

| Category | Tool | Examples |
|----------|------|----------|
| Compiled packages (C/C++/Rust/CUDA) | `conda install -c conda-forge` | `pyarrow`, `rapidfuzz`, `pytorch`, `scikit-learn` (if MKL build desired) |
| Pure-Python packages | `uv pip install` | `requests`, `pandas`, `tqdm`, `python-dotenv`, `PyYAML` |

**Never** run `uv venv` or `uv add` in this project — those create a uv-managed environment that bypasses conda and loses access to conda-installed native libraries. Always use `uv pip` inside the activated conda environment.

**`requirements.txt` contains only pure-Python packages.** Compiled packages are installed separately via conda and are documented above, not listed in the file. This keeps `requirements.txt` free of anything that would trigger a source build on a fresh machine.

## Phases

- Phase 0: Environment + scaffolding — **complete**
- Phase 1: Data foundation — **in progress**
- Phase 2: Features + similarity
- Phase 3: Recommender + evaluation
- Phase 4: API layer + deploy
- Phase 5: UI + integration
- Phase 6: Quality upgrades
- Phase 7: Production hardening
- Phase 8: Portfolio deliverables

## License

TBD.
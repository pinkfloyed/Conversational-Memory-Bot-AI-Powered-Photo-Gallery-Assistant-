from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()


DATASET_DIR = BASE_DIR / "data" / "dataset"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
HISTORY_DIR = BASE_DIR / "static" / "history"
CHROMA_DB_DIR = BASE_DIR / "chromadb_dir"

print(f"BASE_DIR: {BASE_DIR}")
print(f"DATASET_DIR: {DATASET_DIR}")
print(f"UPLOAD_DIR: {UPLOAD_DIR}")
print(f"HISTORY_DIR: {HISTORY_DIR}")
print(f"CHROMA_DB_DIR: {CHROMA_DB_DIR}")


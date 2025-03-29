import os, cv2, torch, chromadb, sys
from pathlib import Path
from config import CHROMA_DB_DIR


sys.path.insert(0, str(Path(__file__).parent.parent))

# Global client instance
_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    return _chroma_client

def get_collection(name="images_metadata_collection"):
    client = get_chroma_client()
    return client.get_or_create_collection(name=name)

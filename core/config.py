from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

MARKETING_DB_PATH = BASE_DIR / "storage/sqlite/marketing.db"

AGENT_MEMORY_DB_PATH = BASE_DIR / "storage/sqlite/agent_memory.db"

CHROMA_PATH = BASE_DIR / "storage/vector/chromadb"


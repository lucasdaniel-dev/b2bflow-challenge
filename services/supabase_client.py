import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from supabase import create_client, Client

#  garante que o .env da raiz sempre será carregado
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger(__name__)

#  variáveis de ambiente
SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str | None = os.getenv("SUPABASE_KEY")
TABLE_NAME: str = os.getenv("SUPABASE_TABLE", "contacts")

#  falha explícita se faltar config
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL ou SUPABASE_KEY não definidos no .env")


def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_contacts(limit: int = 3) -> list[dict[str, Any]]:
    """Busca contatos cadastrados no Supabase, limitado a `limit` registros."""
    try:
        client = get_client()

        response = (
            client
            .table(TABLE_NAME)
            .select("name, phone")
            .limit(limit)
            .execute()
        )

        return response.data or []

    except Exception as e:
        logger.error(f"Erro ao buscar contatos no Supabase: {e}")
        raise
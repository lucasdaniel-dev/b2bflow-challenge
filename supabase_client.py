import logging
import os
from typing import Any

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
logger = logging.getLogger(__name__)

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]
TABLE_NAME: str = os.getenv("SUPABASE_TABLE", "contacts")


def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_contacts(limit: int = 3) -> list[dict[str, Any]]:
    """Busca contatos cadastrados no Supabase, limitado a `limit` registros."""
    try:
        client = get_client()
        response = client.table(TABLE_NAME).select("name, phone").limit(limit).execute()
        return response.data or []
    except KeyError as e:
        logger.error(f"Variável de ambiente ausente: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar contatos no Supabase: {e}")
        raise

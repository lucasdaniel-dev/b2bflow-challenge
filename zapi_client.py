import logging
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

ZAPI_INSTANCE_ID: str = os.environ["ZAPI_INSTANCE_ID"]
ZAPI_TOKEN: str = os.environ["ZAPI_TOKEN"]
ZAPI_CLIENT_TOKEN: str = os.environ["ZAPI_CLIENT_TOKEN"]

BASE_URL: str = (
    f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}"
)


def normalize_phone(phone: str) -> str:
    """Remove caracteres não numéricos e garante código de país (55 para BR)."""
    digits = re.sub(r"\D", "", phone)
    if not digits.startswith("55"):
        digits = "55" + digits
    return digits


def send_whatsapp_message(phone: str, message: str) -> bool:
    """Envia uma mensagem de texto via Z-API. Retorna True se bem-sucedido."""
    normalized = normalize_phone(phone)
    url = f"{BASE_URL}/send-text"
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }
    payload = {"phone": normalized, "message": message}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP ao enviar para {normalized}: {e} | Body: {e.response.text}")
    except requests.exceptions.ConnectionError:
        logger.error(f"Erro de conexão ao tentar enviar para {normalized}.")
    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao enviar para {normalized}.")
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar para {normalized}: {e}")

    return False

import logging
import sys
from services.supabase_client import fetch_contacts
from services.zapi_client import send_whatsapp_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("🚀 Iniciando envio de mensagens via WhatsApp...")

    contacts = fetch_contacts(limit=3)

    if not contacts:
        logger.warning("Nenhum contato encontrado no banco de dados. Encerrando.")
        return

    logger.info(f"{len(contacts)} contato(s) encontrado(s). Iniciando envios...")

    success_count = 0
    failure_count = 0

    for contact in contacts:
        name: str = contact.get("name", "").strip()
        phone: str = contact.get("phone", "").strip()

        if not name or not phone:
            logger.warning(f"Contato com dados incompletos ignorado: {contact}")
            failure_count += 1
            continue

        message = f"Olá, {name} tudo bem com você?"

        sent = send_whatsapp_message(phone=phone, message=message)

        if sent:
            logger.info(f"✅ Mensagem enviada para {name} ({phone})")
            success_count += 1
        else:
            logger.error(f"❌ Falha ao enviar mensagem para {name} ({phone})")
            failure_count += 1

    logger.info(
        f"Concluído. ✅ {success_count} enviado(s) | ❌ {failure_count} falha(s)."
    )


if __name__ == "__main__":
    main()

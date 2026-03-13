import logging
import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

logger = logging.getLogger(__name__)

_client: Client | None = None


def get_supabase_client() -> Client:
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")

        if not url or not key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
            )

        _client = create_client(url, key)
        logger.info("supabase_client_initialized", extra={"url": url})

    return _client

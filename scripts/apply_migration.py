"""
Script auxiliar para aplicar a migration 001_create_tables.sql no Supabase.

USO:
  uv run python scripts/apply_migration.py

REQUISITO:
  SUPABASE_SERVICE_ROLE_KEY deve ser definida no .env
  (chave JWT da aba Project Settings > API > service_role)
"""
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
# Aceita tanto SUPABASE_KEY quanto SUPABASE_SERVICE_ROLE_KEY
SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY", "")

MIGRATION_FILE = "src/infrastructure/migrations/001_create_tables.sql"


def apply_migration():
    with open(MIGRATION_FILE) as f:
        sql = f.read()

    headers = {
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json",
    }

    # Supabase REST API não executa SQL diretamente.
    # Usa a Management API (requer token pessoal) ou conexão direta.
    # Este script verifica se consegue alcançar o endpoint /rest/v1/
    r = httpx.get(f"{SUPABASE_URL}/rest/v1/", headers=headers, timeout=10)

    if r.status_code == 200:
        print("✅ Conexão com Supabase REST API estabelecida.")
        print(
            "\nPara aplicar a migration, acesse o Supabase Dashboard:\n"
            f"  1. Abra: {SUPABASE_URL.replace('.supabase.co', '')}/editor\n"
            "     (ou: https://supabase.com/dashboard > seu projeto > SQL Editor)\n"
            "  2. Cole e execute o conteúdo de:\n"
            f"     {MIGRATION_FILE}\n"
        )
    else:
        print(f"❌ Status {r.status_code}: {r.text[:200]}")
        print(
            "\nVerifique se SUPABASE_KEY no .env é a 'service_role' key\n"
            "(não a 'anon/public' key). Acesse:\n"
            "  Project Settings > API > Project API keys > service_role\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    apply_migration()

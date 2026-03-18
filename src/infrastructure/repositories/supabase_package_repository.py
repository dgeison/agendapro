import logging

from supabase import Client

from src.domain.ports.package_repository import PackageRepository

logger = logging.getLogger(__name__)

TABLE = "student_packages"


class SupabasePackageRepository(PackageRepository):
    def __init__(self, client: Client):
        self._client = client

    def get_student_balance(self, student_id: str) -> int:
        response = (
            self._client.table(TABLE)
            .select("credits_balance")
            .eq("student_id", student_id)
            .maybe_single()
            .execute()
        )

        if response is None or response.data is None:
            logger.info("student_balance_not_found", extra={"student_id": student_id})
            return 0

        balance = response.data["credits_balance"]
        logger.info(
            "student_balance_fetched",
            extra={"student_id": student_id, "balance": balance},
        )
        return balance

    def add_credits(self, student_id: str, amount: int) -> dict:
        """
        Adiciona créditos ao saldo do aluno.
        Usa upsert para criar o registro se não existir ou somar ao saldo existente.
        Como PostgREST não suporta incremento atômico sem RPC, fazemos read-then-write
        (aceitável para MVP; migrar para RPC/trigger em produção se necessário).
        """
        current_response = (
            self._client.table(TABLE)
            .select("id, credits_balance")
            .eq("student_id", student_id)
            .maybe_single()
            .execute()
        )

        if current_response is not None and current_response.data is not None:
            row_id = current_response.data["id"]
            new_balance = current_response.data["credits_balance"] + amount
            response = (
                self._client.table(TABLE)
                .update({"credits_balance": new_balance})
                .eq("id", row_id)
                .execute()
            )
        else:
            response = (
                self._client.table(TABLE)
                .insert({"student_id": student_id, "credits_balance": amount})
                .execute()
            )

        result = response.data[0]
        logger.info(
            "credits_added",
            extra={
                "student_id": student_id,
                "amount": amount,
                "new_balance": result.get("credits_balance"),
            },
        )
        return result

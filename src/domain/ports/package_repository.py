from abc import ABC, abstractmethod


class PackageRepository(ABC):
    @abstractmethod
    def get_student_balance(self, student_id: str) -> int:
        """Retorna o saldo de créditos disponíveis do aluno."""
        raise NotImplementedError

    @abstractmethod
    def add_credits(self, student_id: str, amount: int) -> dict:
        """Adiciona créditos ao saldo do aluno e retorna o registro atualizado."""
        raise NotImplementedError

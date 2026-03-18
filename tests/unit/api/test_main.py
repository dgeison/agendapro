"""
Testes unitários — src/api/main.py
Critério de aceite do Plano 005:
  6. _run_lock_expiry_loop cancela corretamente ao receber CancelledError (sem task leak)
"""
import asyncio

import pytest


class TestRunLockExpiryLoop:
    @pytest.mark.anyio
    async def test_loop_cancels_cleanly_on_cancelled_error(self, monkeypatch):
        """Critério 6: task cancela sem propagar exceção — sem task leak."""
        from src.api.main import _run_lock_expiry_loop

        # Reduzir interval para 0 e mockar o use case para evitar I/O real
        monkeypatch.setenv("LOCK_EXPIRY_INTERVAL_SECONDS", "0")

        execute_calls = []

        class FakeUseCase:
            def execute(self):
                execute_calls.append(1)
                return 0

        import src.api.main as main_module
        monkeypatch.setattr(
            main_module,
            "ExpireSessionLocksUseCase",
            lambda session_repository: FakeUseCase(),
        )
        monkeypatch.setattr(main_module, "get_session_repository", lambda client: None)
        monkeypatch.setattr(main_module, "get_client", lambda: None)

        task = asyncio.create_task(_run_lock_expiry_loop())
        # Deixar o loop rodar ao menos uma iteração
        await asyncio.sleep(0.05)
        task.cancel()

        # Task deve terminar sem levantar exceção não tratada
        with pytest.raises(asyncio.CancelledError):
            await task

        assert task.done()
        assert task.cancelled()

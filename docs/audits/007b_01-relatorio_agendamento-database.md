# Relatório de Auditoria: 007b - Persistência de Agendamentos

**Data:** 2026-03-18 | **Plano:** `docs/plans/007b-agendamento-database.md` | **Status:** ✅ CONCLUÍDO

---

## O que foi implementado

| Artefato | Caminho | Status |
|---|---|---|
| Erro de domínio `SlotAlreadyLockedError` | `src/domain/errors.py` | ✅ Criado |
| Port (Interface) `AppointmentRepository` | `src/domain/ports/appointment_repository.py` | ✅ Criado |
| Adapter `SupabaseAppointmentRepository` | `src/infrastructure/repositories/supabase_appointment_repository.py` | ✅ Criado |
| Testes de integração | `tests/integration/test_supabase_appointment_repository.py` | ✅ Criado (4 testes) |

## Cobertura implementada (código)

- `save(appointment: dict) -> dict` — insere no Supabase, captura `APIError` com código `23505` e relança como `SlotAlreadyLockedError`
- `find_by_time_range(start_time, end_time, professor_id) -> list` — busca agendamentos com sobreposição de horário (condição: `start_time < end AND end_time > start`)

## Resultado dos Testes

```
4 passed, 2 warnings in 1.22s
```

| Teste | Status |
|---|---|
| `test_save_persists_appointment_and_returns_dict` | ✅ PASS |
| `test_save_raises_slot_already_locked_error_on_duplicate` | ✅ PASS |
| `test_find_by_time_range_returns_overlapping_appointments` | ✅ PASS |
| `test_find_by_time_range_returns_empty_for_free_slot` | ✅ PASS |

## Fix aplicado durante a execução

`SlotAlreadyLockedError.__init__` assumia que `start_time`/`end_time` eram objetos `datetime`, mas o repositório passa strings (vindas do dict de appointment). Corrigido com `hasattr(x, "isoformat")` para suportar ambos os tipos.

## Dívida técnica

Nenhuma.

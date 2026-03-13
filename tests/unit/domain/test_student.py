import pytest
from uuid import UUID

from src.domain.entities.student import Student


class TestStudent:
    def test_create_student_with_valid_data(self):
        student = Student(
            name="Maria Oliveira",
            whatsapp="+5511999998888",
        )

        assert isinstance(student.id, UUID)
        assert student.name == "Maria Oliveira"
        assert student.whatsapp == "+5511999998888"
        assert student.email is None

    def test_create_student_with_email(self):
        student = Student(
            name="Carlos Souza",
            whatsapp="+5511977776666",
            email="carlos@example.com",
        )

        assert student.email == "carlos@example.com"

    def test_student_id_is_unique(self):
        s1 = Student(name="Aluno A", whatsapp="+5511111111111")
        s2 = Student(name="Aluno B", whatsapp="+5522222222222")

        assert s1.id != s2.id

    def test_student_whatsapp_is_required(self):
        with pytest.raises(TypeError):
            Student(name="Aluno Inválido")

    def test_student_whatsapp_must_not_be_empty(self):
        with pytest.raises(ValueError, match="whatsapp"):
            Student(name="Aluno Inválido", whatsapp="")

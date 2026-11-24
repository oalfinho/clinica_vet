import unittest

from atendimento import Atendimento
from cadastro import Cadastro


class TestProntuario(unittest.TestCase):
    def test_abre_na_chamada_e_preserva_historico_apos_alta(self):
        cadastro = Cadastro()
        cadastro.cadastrar_tutor("Ana", "001", "9999")
        agenda = Atendimento(cadastro, 1)
        for nome in ("Lua", "Sol"):
            cadastro.cadastrar_animal("001", nome, "gato", "SRD", 3)
        primeira = agenda.chegar("001", "Lua", "Consulta")
        segunda = agenda.chegar("001", "Sol", "Retorno")
        self.assertIsNone(segunda.prontuario)
        ficha = primeira.prontuario
        ficha.medicar("AT", 2)
        ficha.medicar("AT", 1)
        self.assertEqual(ficha.cancelar_medicamento("AT").quantidade, 3)
        ficha.procedimento("Exame", 5000)
        ficha.cancelar_procedimento("Exame")
        self.assertEqual(list(ficha.procedimentos), [])
        agenda.liberar(1)
        self.assertIsNotNone(ficha.alta)
        self.assertEqual([p.numero for p in agenda.historico], [1, 2])
        self.assertIs(segunda.prontuario.chegada.animal, cadastro.buscar_animal("001", "Sol"))

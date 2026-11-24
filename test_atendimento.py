import unittest

from atendimento import Atendimento
from cadastro import Cadastro


class TestAtendimento(unittest.TestCase):
    def setUp(self):
        self.cadastro = Cadastro()
        self.cadastro.cadastrar_tutor("Ana", "001", "9999")
        for nome in ("Lua", "Sol", "Mel", "Luz"):
            self.cadastro.cadastrar_animal("001", nome, "gato", "SRD", 3)

    def test_ordem_de_chamada(self):
        agenda = Atendimento(self.cadastro, 1)
        for nome in ("Lua", "Sol", "Mel", "Luz"):
            agenda.chegar("001", nome, "Avaliação", emergencia=nome in ("Mel", "Luz"))
        sala = next(iter(agenda.consultorios))
        self.assertEqual(sala.atual.animal.nome, "Lua")
        for nome in ("Mel", "Luz", "Sol"):
            self.assertEqual(agenda.liberar(1).animal.nome, nome)
        self.assertIsNone(agenda.liberar(1))

    def test_salas_independentes_e_ordem_normal(self):
        agenda = Atendimento(self.cadastro, 2)
        for nome in ("Lua", "Sol", "Mel", "Luz"):
            agenda.chegar("001", nome, "Retorno")
        self.assertEqual([s.atual.animal.nome for s in agenda.consultorios], ["Lua", "Sol"])
        self.assertEqual(agenda.liberar(2).animal.nome, "Mel")
        self.assertEqual(agenda.liberar(1).animal.nome, "Luz")

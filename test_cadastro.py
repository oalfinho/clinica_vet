import unittest

from cadastro import Cadastro


class TestCadastro(unittest.TestCase):
    def test_animais_com_mesmo_nome_em_tutores_diferentes(self):
        cadastro = Cadastro()
        for cpf in ("001", "002"):
            cadastro.cadastrar_tutor("Ana", cpf, "9999")
            cadastro.cadastrar_animal(cpf, "Lua", "gata", "SRD", 2)
        primeira = cadastro.remover_animal("001", "lua")
        segunda = cadastro.buscar_animal("002", "Lua")
        self.assertIsNot(primeira, segunda)
        with self.assertRaises(ValueError):
            cadastro.buscar_animal("001", "Lua")
        cadastro.remover_tutor("001")
        with self.assertRaises(ValueError):
            cadastro.buscar_tutor("001")
        self.assertIs(cadastro.buscar_animal("002", "Lua"), segunda)

    def test_varios_animais_e_cpf_duplicado(self):
        cadastro = Cadastro()
        tutor = cadastro.cadastrar_tutor("Ana", "001", "9999")
        for nome in ("Lua", "Sol"):
            cadastro.cadastrar_animal("001", nome, "gato", "SRD", 2)
        self.assertEqual([a.nome for a in tutor.animais], ["Lua", "Sol"])
        with self.assertRaises(ValueError):
            cadastro.cadastrar_tutor("Outro", "001", "8888")

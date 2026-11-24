import unittest

from atendimento import Atendimento
from cadastro import Cadastro
from diagnostico import nova_arvore


class TestDiagnostico(unittest.TestCase):
    def test_pre_ordem_e_indentacao(self):
        arvore = nova_arvore()
        linhas = list(arvore.exibir())
        self.assertEqual(len(linhas), 10)
        self.assertEqual(linhas[:4], [
            "Animal — Saudável", "  Sistema digestório — Saudável",
            "    Estômago (D1) — Saudável", "    Intestino (D2) — Saudável"
        ])
        self.assertEqual(linhas[-1], "    Unhas (P2) — Saudável")

    def test_alteracoes_pertencem_a_um_atendimento(self):
        cadastro = Cadastro()
        cadastro.cadastrar_tutor("Ana", "001", "9999")
        cadastro.cadastrar_animal("001", "Lua", "gata", "SRD", 3)
        agenda = Atendimento(cadastro, 1)
        primeiro = agenda.chegar("001", "Lua", "Retorno")
        primeiro.diagnostico.marcar_alterado("p2")
        primeiro.diagnostico.marcar_alterado("Pele")
        self.assertIn("    Unhas (P2) — Alterado", list(primeiro.diagnostico.exibir()))
        agenda.liberar(1)
        segundo = agenda.chegar("001", "Lua", "Consulta")
        self.assertTrue(all(no.estado == "Saudável" for _, no in segundo.diagnostico.pre_ordem()))
        with self.assertRaises(ValueError):
            segundo.diagnostico.marcar_alterado("X9")

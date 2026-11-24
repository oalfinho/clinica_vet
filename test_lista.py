import unittest

from lista import Lista


class TestLista(unittest.TestCase):
    def setUp(self):
        self.lista = Lista()
        for nome in ("Lua", "Sol", "Mel"):
            self.lista.adicionar(nome)

    def test_busca_e_ordem_de_insercao(self):
        self.assertEqual(list(self.lista), ["Lua", "Sol", "Mel"])
        self.assertEqual(self.lista.buscar(lambda nome: nome.startswith("M")), "Mel")

    def test_remover_do_meio_preserva_os_vizinhos(self):
        removido = self.lista.remover(lambda nome: nome == "Sol")
        self.assertEqual(removido, "Sol")
        self.assertEqual(list(self.lista), ["Lua", "Mel"])

    def test_remover_das_pontas_e_reutilizar_lista(self):
        for alvo in ("Lua", "Mel", "Sol"):
            self.lista.remover(lambda nome: nome == alvo)
        self.assertIsNone(self.lista.inicio)
        self.assertIsNone(self.lista.fim)
        self.lista.adicionar("Luz")
        self.assertEqual(list(self.lista), ["Luz"])

    def test_nome_ausente(self):
        with self.assertRaises(ValueError):
            self.lista.buscar(lambda nome: nome == "Luz")
        with self.assertRaises(ValueError):
            self.lista.remover(lambda nome: nome == "Luz")
        self.assertEqual(list(self.lista), ["Lua", "Sol", "Mel"])

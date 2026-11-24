import unittest
from datetime import date, timedelta

from estoque import Estoque, Lote, Pedido


class TestEstoque(unittest.TestCase):
    def setUp(self):
        self.estoque = Estoque()
        self.estoque.cadastrar("AT", "Atadura", 3)

    def receber(self, numero, dias, validade, preco, quantidade):
        hoje = date.today()
        lote = Lote(numero, "Fornecedor", hoje - timedelta(days=dias),
                    hoje + timedelta(days=validade), 300, preco, quantidade)
        self.estoque.receber("AT", lote)

    def test_baixa_segue_compra_e_preserva_precos(self):
        self.receber("novo", 1, 10, 700, 3)
        self.receber("antigo", 4, 20, 500, 2)
        consumo = self.estoque.baixar([Pedido("AT", 3)])
        self.assertEqual([(c.lote, c.quantidade, c.preco) for c in consumo],
                         [("antigo", 2, 500), ("novo", 1, 700)])
        self.assertEqual(self.estoque.produto("AT").lotes.frente().quantidade, 2)

    def test_validade_ajuste_e_minimo(self):
        self.receber("vence-hoje", 3, 0, 500, 4)
        self.receber("vencido", 2, -1, 500, 10)
        self.estoque.ajustar("AT", "vence-hoje", 3)
        self.assertEqual(list(self.estoque.alertas()), [])
        self.estoque.ajustar("AT", "vence-hoje", 2)
        self.assertEqual(len(list(self.estoque.alertas())), 1)
        self.assertEqual([(p.lote, p.quantidade) for p in self.estoque.perdas], [("vencido", 10)])

    def test_erro_nao_debita_os_itens_anteriores(self):
        self.receber("unico", 1, 10, 500, 3)
        self.estoque.cadastrar("VAC", "Vacina", 1)
        for outro in (Pedido("VAC", 1), Pedido("AT", 2), Pedido("VAC", -1)):
            with self.assertRaises(ValueError):
                self.estoque.baixar([Pedido("AT", 2), outro])
            self.assertEqual(self.estoque.produto("AT").lotes.frente().quantidade, 3)

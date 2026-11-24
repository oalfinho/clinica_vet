import unittest
from datetime import date

from atendimento import Atendimento
from cadastro import Cadastro
from estoque import Estoque, Lote
from pagamento import fechar


class TestPagamento(unittest.TestCase):
    def setUp(self):
        cadastro = Cadastro()
        cadastro.cadastrar_tutor("Ana", "001", "9999")
        cadastro.cadastrar_animal("001", "Lua", "gato", "SRD", 3)
        self.agenda = Atendimento(cadastro, 1)
        self.ficha = self.agenda.chegar("001", "Lua", "Consulta").prontuario
        self.estoque = Estoque()
        self.estoque.cadastrar("AT", "Atadura", 1)
        hoje = date.today()
        self.lote = Lote("A", "Fornecedor", hoje, hoje, 300, 500, 2)
        self.estoque.receber("AT", self.lote)
        self.ficha.medicar("AT", 1)
        self.ficha.procedimento("Curativo", 3000)

    def test_alta_cartao_e_tentativa_de_repetir(self):
        with self.assertRaises(ValueError):
            fechar(self.ficha, self.estoque, "Ana", "cartão", 2)
        self.agenda.liberar(1)
        recibo = fechar(self.ficha, self.estoque, "Ana", "cartão", 2)
        self.assertEqual((recibo.medicamentos, recibo.procedimentos, recibo.total),
                         (500, 3000, 3500))
        self.assertEqual(recibo.parcelas, 2)
        self.assertEqual(next(iter(self.ficha.consumo)).lote, "A")
        with self.assertRaises(ValueError):
            fechar(self.ficha, self.estoque, "Ana", "cartão")
        with self.assertRaises(ValueError):
            self.ficha.cancelar_procedimento("Curativo")
        self.assertEqual(self.lote.quantidade, 1)

    def test_corrigir_e_tentar_novamente(self):
        self.agenda.liberar(1)
        self.ficha.medicar("AT", 5)
        with self.assertRaises(ValueError):
            fechar(self.ficha, self.estoque, "Ana", "PIX")
        self.ficha.cancelar_medicamento("AT")
        with self.assertRaises(ValueError):
            fechar(self.ficha, self.estoque, "Ana", "PIX", 2)
        self.assertIsNone(self.ficha.pagamento)
        recibo = fechar(self.ficha, self.estoque, "Ana", "dinheiro")
        self.assertEqual(recibo.total, 3000)
        self.assertEqual(self.lote.quantidade, 2)

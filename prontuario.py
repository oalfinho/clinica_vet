from dataclasses import dataclass
from datetime import datetime

from estoque import Pedido, inteiro
from lista import Lista


@dataclass(frozen=True)
class Procedimento:
    nome: str
    valor: int


class Prontuario:
    def __init__(self, numero, chegada, veterinario):
        self.numero = numero
        self.chegada = chegada
        self.veterinario = veterinario
        self.abertura = datetime.now()
        self.alta = None
        self.pagamento = None
        self.consumo = Lista()
        self.medicamentos = Lista()
        self.procedimentos = Lista()

    def verificar_aberto(self):
        if self.pagamento is not None:
            raise ValueError("Prontuário já fechado.")

    def medicar(self, codigo, quantidade):
        self.verificar_aberto()
        inteiro(quantidade, 1)
        for pedido in self.medicamentos:
            if pedido.codigo == codigo:
                quantidade += pedido.quantidade
                self.cancelar_medicamento(codigo)
                break
        self.medicamentos.adicionar(Pedido(codigo, quantidade))

    def cancelar_medicamento(self, codigo):
        self.verificar_aberto()
        return self.medicamentos.remover(lambda pedido: pedido.codigo == codigo)

    def procedimento(self, nome, valor):
        self.verificar_aberto()
        inteiro(valor, 0)
        self.procedimentos.adicionar(Procedimento(nome, valor))

    def cancelar_procedimento(self, nome):
        self.verificar_aberto()
        return self.procedimentos.remover(lambda procedimento: procedimento.nome == nome)

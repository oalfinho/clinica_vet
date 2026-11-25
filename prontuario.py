from dataclasses import dataclass
from datetime import datetime

from typing import TYPE_CHECKING, Optional

from estoque import Consumo, Pedido, inteiro
from lista import Lista
from pagamento import Pagamento

if TYPE_CHECKING:
    from atendimento import Chegada


@dataclass(frozen=True)
class Procedimento:
    nome: str
    valor: int


class Prontuario:
    def __init__(self, numero: int, chegada: "Chegada", veterinario: str):
        self.numero = numero
        self.chegada = chegada
        self.veterinario = veterinario
        self.abertura = datetime.now()
        self.alta: Optional[datetime] = None
        self.pagamento: Optional[Pagamento] = None
        self.consumo: Lista[Consumo] = Lista()
        self.medicamentos: Lista[Pedido] = Lista()
        self.procedimentos: Lista[Procedimento] = Lista()

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

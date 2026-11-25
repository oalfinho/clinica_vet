from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, Tuple
from fila import Fila
from lista import Lista


def inteiro(valor, minimo):
    if type(valor) is not int or valor < minimo:
        raise ValueError(f"Informe um inteiro a partir de {minimo}.")


@dataclass
class Lote:
    numero: str
    fornecedor: str
    compra: date
    validade: date
    custo: int  # Valores monetários em centavos.
    preco: int
    quantidade: int


@dataclass(frozen=True)
class Pedido:
    codigo: str
    quantidade: int


@dataclass
class Produto:
    codigo: str
    nome: str
    minimo: int
    lotes: Fila[Lote] = field(default_factory=Fila)


@dataclass(frozen=True)
class Perda:
    dia: date
    produto: str
    lote: str
    quantidade: int
    custo_unitario: int


@dataclass(frozen=True)
class Consumo:
    produto: str
    lote: str
    quantidade: int
    preco: int


class Estoque:
    def __init__(self):
        self.produtos: Lista[Produto] = Lista()
        self.perdas: Lista[Perda] = Lista()

    def cadastrar(self, codigo, nome, minimo):
        inteiro(minimo, 0)
        if any(p.codigo == codigo for p in self.produtos):
            raise ValueError("Código já cadastrado.")
        self.produtos.adicionar(Produto(codigo, nome, minimo))

    def produto(self, codigo):
        return self.produtos.buscar(lambda p: p.codigo == codigo)

    def receber(self, codigo: str, lote: Lote):
        produto = self.produto(codigo)
        inteiro(lote.quantidade, 1)
        inteiro(lote.custo, 0)
        inteiro(lote.preco, 0)
        if lote.compra > date.today() or lote.validade < lote.compra:
            raise ValueError("Datas do lote incompatíveis.")
        if any(l.numero == lote.numero for l in produto.lotes):
            raise ValueError("Lote já presente.")
        # Um lançamento atrasado também precisa respeitar a data da compra.
        ordenada: Fila[Lote] = Fila()
        while not produto.lotes.vazia() and produto.lotes.frente().compra <= lote.compra:
            ordenada.entrar(produto.lotes.sair())
        ordenada.entrar(lote)
        while not produto.lotes.vazia():
            ordenada.entrar(produto.lotes.sair())
        produto.lotes = ordenada

    def descartar_vencidos(self):
        hoje = date.today()
        for produto in self.produtos:
            validos: Fila[Lote] = Fila()
            while not produto.lotes.vazia():
                lote = produto.lotes.sair()
                if lote.validade < hoje:
                    self.perdas.adicionar(Perda(hoje, produto.codigo, lote.numero,
                                                 lote.quantidade, lote.custo))
                else:
                    validos.entrar(lote)
            produto.lotes = validos

    def ajustar(self, codigo, numero, quantidade):
        inteiro(quantidade, 0)
        self.descartar_vencidos()
        for lote in self.produto(codigo).lotes:
            if lote.numero == numero:
                lote.quantidade = quantidade
                return
        raise ValueError("Lote não encontrado.")

    def alertas(self):
        self.descartar_vencidos()
        for produto in self.produtos:
            total = sum(lote.quantidade for lote in produto.lotes)
            if total < produto.minimo:
                yield f"{produto.nome}: {total} em estoque, mínimo {produto.minimo}."

    def baixar(self, pedidos: Iterable[Pedido]) -> Lista[Consumo]:
        self.descartar_vencidos()
        plano: Lista[Tuple[Produto, Lote, int]] = Lista()
        codigos: Lista[str] = Lista()
        for pedido in pedidos:
            inteiro(pedido.quantidade, 1)
            if any(codigo == pedido.codigo for codigo in codigos):
                raise ValueError("Agrupe as quantidades do mesmo produto.")
            codigos.adicionar(pedido.codigo)
            produto = self.produto(pedido.codigo)
            faltam = pedido.quantidade
            for lote in produto.lotes:
                usar = min(faltam, lote.quantidade)
                if usar:
                    plano.adicionar((produto, lote, usar))
                    faltam -= usar
                if faltam == 0:
                    break
            if faltam:
                raise ValueError(f"Saldo insuficiente de {produto.nome}.")
        consumo: Lista[Consumo] = Lista()
        for produto, lote, usar in plano:  # Só altera saldos após validar todos os pedidos.
            lote.quantidade -= usar
            consumo.adicionar(Consumo(produto.codigo, lote.numero, usar, lote.preco))
            while not produto.lotes.vazia() and produto.lotes.frente().quantidade == 0:
                produto.lotes.sair()
        return consumo

from typing import Callable, Generic, Iterator, Optional

from noh import No, T


class Lista(Generic[T]):
    """Lista simplesmente encadeada, com acesso às duas pontas."""
    def __init__(self):
        self.inicio: Optional[No[T]] = None
        self.fim: Optional[No[T]] = None

    def __iter__(self) -> Iterator[T]:
        atual = self.inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def adicionar(self, valor: T) -> None:
        novo = No(valor)
        if self.fim is None:
            self.inicio = novo
        else:
            self.fim.proximo = novo
        self.fim = novo

    def buscar(self, criterio: Callable[[T], bool]) -> T:
        for valor in self:
            if criterio(valor):
                return valor
        raise ValueError("Registro não encontrado.")

    def remover(self, criterio: Callable[[T], bool]) -> T:
        anterior = None
        atual = self.inicio
        while atual is not None:
            if criterio(atual.valor):
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual is self.fim:
                    self.fim = anterior
                return atual.valor
            anterior, atual = atual, atual.proximo
        raise ValueError("Registro não encontrado.")

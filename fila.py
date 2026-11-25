from typing import Generic, Iterator

from lista import Lista
from noh import T


class Fila(Generic[T]):
    def __init__(self):
        self._dados: Lista[T] = Lista()

    def entrar(self, item: T) -> None:
        self._dados.adicionar(item)

    def vazia(self):
        return self._dados.inicio is None

    def frente(self) -> T:
        inicio = self._dados.inicio
        if inicio is None:
            raise ValueError("Fila vazia.")
        return inicio.valor

    def sair(self) -> T:
        return self._dados.remover(lambda item: True)

    def __iter__(self) -> Iterator[T]:
        return iter(self._dados)

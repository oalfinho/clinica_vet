from lista import Lista


class Fila:
    def __init__(self):
        self._dados = Lista()

    def entrar(self, item):
        self._dados.adicionar(item)

    def vazia(self):
        return self._dados.inicio is None

    def frente(self):
        if self.vazia():
            raise ValueError("Fila vazia.")
        return self._dados.inicio.valor

    def sair(self):
        return self._dados.remover(lambda item: True)

    def __iter__(self):
        return iter(self._dados)

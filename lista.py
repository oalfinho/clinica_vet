from noh import No


class Lista:
    """Lista simplesmente encadeada, com acesso às duas pontas."""
    def __init__(self):
        self.inicio = self.fim = None

    def __iter__(self):
        atual = self.inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def adicionar(self, valor):
        novo = No(valor)
        if self.fim is None:
            self.inicio = novo
        else:
            self.fim.proximo = novo
        self.fim = novo

    def buscar(self, criterio):
        for valor in self:
            if criterio(valor):
                return valor
        raise ValueError("Registro não encontrado.")

    def remover(self, criterio):
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

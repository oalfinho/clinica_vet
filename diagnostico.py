from lista import Lista


class EstruturaAnimal:
    def __init__(self, nome, codigo=None):
        self.nome = nome
        self.codigo = codigo
        self.estado = "Saudável"
        self.filhos = Lista()

    def adicionar(self, nome, codigo=None):
        filho = EstruturaAnimal(nome, codigo)
        self.filhos.adicionar(filho)
        return filho  # Permite acrescentar partes a este novo ramo.

    def pre_ordem(self, nivel=0):
        yield nivel, self  # Visita o pai antes de descer aos filhos.
        for filho in self.filhos:
            yield from filho.pre_ordem(nivel + 1)

    def marcar_alterado(self, identificador):
        chave = identificador.strip().casefold()
        for _, no in self.pre_ordem():
            if no.nome.casefold() == chave or (no.codigo and no.codigo.casefold() == chave):
                no.estado = "Alterado"
                return no
        raise ValueError("Estrutura não encontrada.")

    def exibir(self):
        for nivel, no in self.pre_ordem():
            codigo = f" ({no.codigo})" if no.codigo else ""
            yield "  " * nivel + f"{no.nome}{codigo} — {no.estado}"


def nova_arvore():
    raiz = EstruturaAnimal("Animal")
    digestorio = raiz.adicionar("Sistema digestório")
    digestorio.adicionar("Estômago", "D1")
    digestorio.adicionar("Intestino", "D2")
    respiratorio = raiz.adicionar("Sistema respiratório")
    respiratorio.adicionar("Pulmões", "R1")
    respiratorio.adicionar("Traqueia", "R2")
    pele = raiz.adicionar("Pele")
    pele.adicionar("Pelos", "P1")
    pele.adicionar("Unhas", "P2")
    return raiz

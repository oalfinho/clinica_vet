from dataclasses import dataclass, field
from lista import Lista


@dataclass
class Animal:
    nome: str
    especie: str
    raca: str
    idade: int


@dataclass
class Tutor:
    nome: str
    cpf: str
    telefone: str
    animais: Lista[Animal] = field(default_factory=Lista)  # Cada tutor recebe sua própria lista.


class Cadastro:
    def __init__(self):
        self.tutores: Lista[Tutor] = Lista()

    def cadastrar_tutor(self, nome, cpf, telefone):
        if any(tutor.cpf == cpf for tutor in self.tutores):
            raise ValueError("CPF já cadastrado.")
        tutor = Tutor(nome, cpf, telefone)
        self.tutores.adicionar(tutor)
        return tutor

    def buscar_tutor(self, cpf):
        return self.tutores.buscar(lambda tutor: tutor.cpf == cpf)

    def remover_tutor(self, cpf):
        return self.tutores.remover(lambda tutor: tutor.cpf == cpf)

    def cadastrar_animal(self, cpf, nome, especie, raca, idade):
        animais = self.buscar_tutor(cpf).animais
        if idade < 0:
            raise ValueError("Idade inválida.")
        if any(animal.nome.casefold() == nome.casefold() for animal in animais):
            raise ValueError("Animal já cadastrado para este tutor.")
        animal = Animal(nome, especie, raca, idade)
        animais.adicionar(animal)
        return animal

    def buscar_animal(self, cpf, nome):
        animais = self.buscar_tutor(cpf).animais
        return animais.buscar(lambda animal: animal.nome.casefold() == nome.casefold())

    def remover_animal(self, cpf, nome):
        animais = self.buscar_tutor(cpf).animais
        return animais.remover(lambda animal: animal.nome.casefold() == nome.casefold())

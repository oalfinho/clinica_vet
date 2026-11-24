from dataclasses import dataclass, field
from datetime import datetime

from cadastro import Animal, Tutor
from diagnostico import EstruturaAnimal, nova_arvore
from fila import Fila
from lista import Lista
from prontuario import Prontuario


@dataclass
class Chegada:
    tutor: Tutor
    animal: Animal
    queixa: str
    emergencia: bool
    hora: datetime = field(default_factory=datetime.now)
    diagnostico: EstruturaAnimal = field(default_factory=nova_arvore)
    prontuario: Prontuario = field(default=None, init=False, repr=False, compare=False)


@dataclass
class Consultorio:
    numero: int
    atual: Chegada = None
    veterinario: str = ""


class Atendimento:
    def __init__(self, cadastro, quantidade_consultorios):
        if quantidade_consultorios < 1:
            raise ValueError("É preciso ter pelo menos um consultório.")
        self.cadastro = cadastro
        self.normal = Fila()
        self.emergencia = Fila()
        self.historico = Lista()
        self.proximo_numero = 1
        self.consultorios = Lista()
        for numero in range(1, quantidade_consultorios + 1):
            self.consultorios.adicionar(Consultorio(numero, veterinario=f"Veterinário do consultório {numero}"))

    def chegar(self, cpf, nome, queixa, emergencia=False):
        tutor = self.cadastro.buscar_tutor(cpf)
        animal = self.cadastro.buscar_animal(cpf, nome)
        for fila in (self.normal, self.emergencia):
            if any(chegada.animal is animal for chegada in fila):
                raise ValueError("Animal já está na espera.")
        if any(s.atual and s.atual.animal is animal for s in self.consultorios):
            raise ValueError("Animal já está em atendimento.")
        chegada = Chegada(tutor, animal, queixa, emergencia)
        fila = self.emergencia if emergencia else self.normal
        fila.entrar(chegada)
        for sala in self.consultorios:
            if sala.atual is None:
                self._chamar(sala)
                break
        return chegada

    def _chamar(self, sala):
        fila = self.normal if self.emergencia.vazia() else self.emergencia
        sala.atual = None if fila.vazia() else fila.sair()
        if sala.atual is not None:
            ficha = Prontuario(self.proximo_numero, sala.atual, sala.veterinario)
            sala.atual.prontuario = ficha
            self.historico.adicionar(ficha)
            self.proximo_numero += 1
        return sala.atual

    def liberar(self, numero):
        sala = self.consultorios.buscar(lambda s: s.numero == numero)
        if sala.atual is None:
            raise ValueError("Consultório já está livre.")
        sala.atual.prontuario.alta = datetime.now()
        return self._chamar(sala)

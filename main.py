from datetime import date, timedelta

from atendimento import Atendimento
from cadastro import Cadastro
from estoque import Estoque, Lote
from pagamento import fechar


def reais(centavos):
    return f"R$ {centavos // 100},{centavos % 100:02d}"


def demonstrar():
    cadastro = Cadastro()
    cpf = "00000000000"
    cadastro.cadastrar_tutor("Ana", cpf, "0000-0000")
    for nome in ("Lua", "Sol", "Mel"):
        cadastro.cadastrar_animal(cpf, nome, "cão", "SRD", 3)
    agenda = Atendimento(cadastro, 1)
    sala = next(iter(agenda.consultorios))
    sala.veterinario = "Dra. Lia"

    hoje = date.today()
    estoque = Estoque()
    estoque.cadastrar("AT", "Atadura", 3)
    for numero, dias, quantidade, preco in (("A", 7, 2, 500), ("B", 2, 3, 700)):
        lote = Lote(numero, "Fornecedor A", hoje - timedelta(days=dias),
                    hoje + timedelta(days=90), 300, preco, quantidade)
        estoque.receber("AT", lote)

    lua = agenda.chegar(cpf, "Lua", "Ferimento na pata")
    agenda.chegar(cpf, "Sol", "Retorno")
    agenda.chegar(cpf, "Mel", "Acidente", emergencia=True)
    ficha = lua.prontuario
    print(f"Ficha {ficha.numero}: {lua.animal.nome}, tutora {lua.tutor.nome}, {ficha.veterinario}")
    print("Em espera: Sol (normal), Mel (emergência)")
    lua.diagnostico.marcar_alterado("P2")
    for linha in lua.diagnostico.exibir():
        print(linha)
    ficha.medicar("AT", 3)
    ficha.procedimento("Curativo", 3000)
    ficha.procedimento("Exame", 5000)
    ficha.cancelar_procedimento("Exame")
    proxima = agenda.liberar(1)
    print("Alta de Lua. Próxima chamada:", proxima.animal.nome)
    recibo = fechar(ficha, estoque, "Ana", "cartão", 2)
    for item in ficha.consumo:
        print(f"Lote {item.lote}: {item.quantidade} × {reais(item.preco)}")
    print(f"Materiais: {reais(recibo.medicamentos)} | Procedimentos: {reais(recibo.procedimentos)}")
    print(f"Total: {reais(recibo.total)} no {recibo.forma}, em {recibo.parcelas} parcelas")
    for aviso in estoque.alertas():
        print(aviso)
    while sala.atual is not None:
        ficha = sala.atual.prontuario
        ficha.procedimento("Consulta", 4000)
        agenda.liberar(1)
        recibo = fechar(ficha, estoque, "Ana", "PIX")
        print(f"Ficha {ficha.numero} encerrada: {ficha.chegada.animal.nome}, {reais(recibo.total)}")


if __name__ == "__main__":
    demonstrar()

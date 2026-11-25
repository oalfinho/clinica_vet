from dataclasses import dataclass
from datetime import datetime

from typing import TYPE_CHECKING

from estoque import Estoque, inteiro

if TYPE_CHECKING:
    from prontuario import Prontuario


@dataclass(frozen=True)
class Pagamento:
    prontuario: int
    pagador: str
    forma: str
    parcelas: int
    medicamentos: int
    procedimentos: int
    total: int
    hora: datetime


def fechar(ficha: "Prontuario", estoque: Estoque, pagador: str, forma: str, parcelas: int = 1) -> Pagamento:
    ficha.verificar_aberto()
    if ficha.alta is None:
        raise ValueError("O fechamento exige alta.")
    if not pagador.strip() or forma not in ("PIX", "cartão", "dinheiro"):
        raise ValueError("Informe o pagador e uma forma de pagamento válida.")
    inteiro(parcelas, 1)
    if forma != "cartão" and parcelas != 1:
        raise ValueError("Somente cartão permite parcelamento.")
    procedimentos = sum(p.valor for p in ficha.procedimentos)
    consumo = estoque.baixar(ficha.medicamentos)
    medicamentos = sum(item.preco * item.quantidade for item in consumo)
    recibo = Pagamento(ficha.numero, pagador, forma, parcelas, medicamentos,
                       procedimentos, medicamentos + procedimentos, datetime.now())
    ficha.consumo = consumo
    ficha.pagamento = recibo
    return recibo

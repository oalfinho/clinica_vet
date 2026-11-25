# Clínica Veterinária

**Estrutura de Dados · Fatec Rio Claro · Prof. Orlando**

[Assistir à demonstração da clínica (MP4, 3min34s)](./clinica_legendada.mp4)

Legendas elaboradas e inseridas com auxílio de IA.

## 1. Concepção do projeto

A clínica tem um número limitado de consultórios. Enquanto um animal está em consulta, outros aguardam. O sistema precisa decidir quem entra a seguir, registrar o que foi feito e cobrar os materiais pelo preço dos lotes utilizados.

A simulação acompanha três cães da tutora Ana. Lua chega com um ferimento na pata, Sol aguarda um retorno e Mel chega após um acidente. Esse cenário permite observar duas decisões no terminal: por que Mel é chamada antes de Sol e de onde vêm os R$ 47 cobrados no atendimento de Lua.

## 2. Como executar

Com Python 3 instalado, abra o terminal na pasta que contém `main.py`. O projeto usa apenas a biblioteca padrão do Python.

| Ambiente | Comando |
|---|---|
| Windows (PowerShell) | `py main.py` |
| Linux ou macOS | `python3 main.py` |

O comando executa a demonstração completa automaticamente. Os dados ficam em memória e são recriados a cada execução. No terminal, acompanhe a árvore de diagnóstico, a chamada de Mel, a saída de ataduras dos lotes A e B e o encerramento das três fichas.

## 3. Organização do código

As estruturas genéricas ficam em módulos próprios. Assim, a mesma lista encadeada serve para guardar animais, percorrer lotes e organizar os filhos de um nó da árvore.

| Arquivo | Classes ou funções principais | Responsabilidade |
|---|---|---|
| `noh.py` | `No` | Guardar um valor e a referência ao próximo nó. |
| `lista.py` | `Lista` | Inserir no fim, percorrer, buscar e remover por critério. |
| `fila.py` | `Fila` | Inserir no fim e retirar da frente, usando a lista encadeada. |
| `cadastro.py` | `Cadastro`, `Tutor`, `Animal` | Cadastrar, localizar e remover tutores e animais. |
| `atendimento.py` | `Atendimento`, `Chegada`, `Consultorio` | Registrar a chegada, organizar a espera, abrir a ficha na chamada e liberar a sala na alta. |
| `diagnostico.py` | `EstruturaAnimal`, `nova_arvore` | Construir a hierarquia, exibi-la e marcar alterações. |
| `estoque.py` | `Estoque`, `Produto`, `Lote`, `Pedido`, `Consumo`, `Perda` | Receber compras, ajustar inventário, controlar validade e registrar saídas por lote. |
| `prontuario.py` | `Prontuario`, `Procedimento` | Registrar e cancelar itens até o fechamento da ficha. |
| `pagamento.py` | `Pagamento`, `fechar` | Validar a alta, efetivar a baixa e registrar o pagamento. |
| `main.py` | `demonstrar` | Executar o cenário de Lua, Sol e Mel. |

## 4. Árvore de sistemas do animal

Cada chegada recebe uma árvore própria, criada por `nova_arvore()`. Cada nó tem um nome, um estado e uma lista de filhos. As folhas também têm um código. A demonstração chama `marcar_alterado("P2")` na árvore de Lua. O resultado exibido é:

```text
Animal — Saudável
  Sistema digestório — Saudável
    Estômago (D1) — Saudável
    Intestino (D2) — Saudável
  Sistema respiratório — Saudável
    Pulmões (R1) — Saudável
    Traqueia (R2) — Saudável
  Pele — Saudável
    Pelos (P1) — Saudável
    Unhas (P2) — Alterado
```

O estado pertence ao nó selecionado. Por isso, marcar Unhas mantém Pele com o estado anterior. O método `pre_ordem` visita primeiro o nó atual e depois cada filho. O nível da visita determina o recuo usado por `exibir`.

## 5. Combinações de estruturas

### 5.1 Atendimento com prioridade — fila de emergência e fila normal

`Atendimento.chegar` escolhe a fila pela categoria da chegada. Quando a sala fica livre, `Atendimento.liberar` chama `_chamar`, que consulta a fila de emergência primeiro. Cada fila mantém a ordem de chegada entre os seus animais.

Na simulação, Lua conclui sua consulta normalmente. A prioridade decide a **próxima vaga**: Mel entra antes de Sol. Em uma fila FIFO única, Sol estaria na frente e seria preciso procurar ou reposicionar a emergência.

### 5.2 Tutores e animais — lista dentro de lista

`Cadastro.buscar_animal(cpf, nome)` encontra o tutor pelo CPF e depois percorre apenas `Tutor.animais`. `cadastrar_animal` e `remover_animal` usam o mesmo vínculo. Dois tutores podem ter uma gata chamada Lua, e cada um pode cadastrar novos animais ao longo do tempo.

Uma lista plana de animais exigiria conferir o vínculo com o tutor em cada busca e precisaria de outra forma de representar tutores que ainda não têm animais.

### 5.3 Estoque — lista de produtos e fila de lotes

`Estoque.produto` localiza o código na lista de produtos. Cada `Produto` guarda sua própria fila de lotes. `receber` mantém a ordem de compra, inclusive quando uma compra antiga é cadastrada depois. `baixar` percorre a fila daquele produto a partir do lote mais antigo.

Em uma fila global, o primeiro lote poderia ser de outro produto. Guardar apenas o saldo total também apagaria a informação necessária para calcular o preço da saída. No caso de Lua, as três ataduras têm o mesmo código, mas saem de dois lotes com preços diferentes.

### 5.4 Diagnóstico — árvore e lista de filhos

Em `EstruturaAnimal.adicionar`, o novo filho entra na lista daquele nó. `pre_ordem` percorre essas listas recursivamente. A raiz tem três filhos e as folhas têm zero. Uma árvore binária imporia o limite de dois filhos. Uma lista plana precisaria guardar o parentesco separadamente para reconstruir os ramos.

### 5.5 Prontuário — medicamentos e procedimentos

`Prontuario.medicar` guarda código e quantidade de produto. `Prontuario.procedimento` guarda nome e valor do serviço. As listas são separadas porque apenas os produtos precisam ser baixados por lote. Uma coleção única exigiria distinguir os tipos a cada cancelamento ou cobrança.

No exemplo, o curativo e o exame entram na ficha. Depois, `cancelar_procedimento("Exame")` remove apenas o exame. O curativo permanece no recibo.

### 5.6 Fechamento — prontuário, estoque e pagamento

A função `fechar` verifica a alta e chama `Estoque.baixar`. A baixa planeja a retirada de todos os itens antes de debitar as quantidades consumidas. Se faltar um produto, a ficha continua aberta para correção. Após o fechamento, a ficha guarda o pagamento e os registros de consumo por lote. Pela chegada associada a ela, é possível identificar o animal e o tutor.

| Item na ficha de Lua | Cálculo | Valor |
|---|---:|---:|
| Ataduras do lote A | 2 × R$ 5,00 | R$ 10,00 |
| Atadura do lote B | 1 × R$ 7,00 | R$ 7,00 |
| Curativo | 1 × R$ 30,00 | R$ 30,00 |
| **Total no cartão, em duas parcelas** | | **R$ 47,00** |

Guardar apenas o total pago impediria conferir quais lotes foram consumidos. Os valores são calculados em centavos. O sistema aceita PIX, dinheiro e cartão, com parcelamento disponível para cartão.

## 6. Complexidade das principais operações

| Operação | Custo no pior caso | Motivo |
|---|---|---|
| Adicionar no fim da lista | O(1) | A lista guarda a referência ao último nó. |
| Buscar ou remover por critério | O(n) | Pode ser preciso visitar todos os nós. |
| Entrar, consultar a frente ou sair da fila | O(1) | A operação usa uma das duas pontas. |
| Escolher a fila prioritária e retirar o próximo | O(1) | Basta verificar se a fila de emergência está vazia e retirar da frente da fila escolhida. |
| Buscar animal por CPF e nome | O(T + A) | Percorre até T tutores e até A animais do tutor localizado. |
| Receber um lote e inseri-lo em ordem de compra | O(P + L) | Busca entre P produtos e percorre até L lotes daquele produto. |
| Descartar lotes vencidos | O(P + B) | Visita P produtos e B lotes no estoque inteiro. |
| Visitar ou marcar um nó da árvore | O(N) | Pode percorrer os N nós. A recursão ocupa O(H) espaço para altura H. |

O custo constante da escolha da fila é só uma parte do atendimento. A chegada completa também consulta o cadastro, verifica duplicatas nas filas e procura um consultório disponível.

## 7. Sustentabilidade

**Ambiental.** Ao descartar um lote vencido, o sistema registra produto, lote e quantidade perdida. Esses dados permitem identificar desperdício nas compras da clínica.

**Econômica.** O consumo por lote permite conferir a cobrança e o saldo restante. Ao final do atendimento de Lua, restam duas ataduras. Como o mínimo cadastrado é três, o terminal exibe o alerta de reposição.

**Social.** A fila de emergência reduz a espera de animais em situação urgente e preserva a ordem de chegada dentro de cada categoria.

## 8. Desenvolvimento incremental

| Etapa | Entrega registrada |
|---|---|
| Estruturas básicas | Nó e lista encadeada com inserção, busca e remoção. |
| Cadastro e recepção | Tutores com suas listas de animais, consultórios e duas filas de espera. |
| Diagnóstico e estoque | Árvore de sistemas, recebimento de lotes, controle de validade e saída por ordem de compra. |
| Prontuário e pagamento | Abertura na chamada, alta, cancelamentos, baixa por lote e fechamento. |
| Demonstração | Integração das etapas no cenário executável de Lua, Sol e Mel. |

[Consultar o histórico de commits da main](https://github.com/oalfinho/clinica_vet/commits/main/)

## Why

**Origem: PRD-02**, com `RF-02-10`. Do núcleo, atende `RF-01-62`, `RN-01-43` e `RN-01-54`.

`Trilha.poder_id` é obrigatório, e **nenhum poder existe no banco nem pode ser criado**:
`poderes/regra.py` tem `cadastrar_poder`, `alterar_poder`, `desativar_poder` e
`buscar_poder_do_territorio` escritos e exercitados só por teste de unidade, sem `rotas.py`; a
semeadura de implantação converge chaves e o Admin fundador, e não toca o catálogo. Com isso a
autoria da trilha do PRD-09 é inalcançável e o crédito da coleta depende de um poder que
ninguém tem como cadastrar — `RN-08-15` recusa a gravação com 409 enquanto o catálogo não
tiver o poder do papel do Território.

`RF-02-10` — o Admin mantém o catálogo de poderes do ciclo — é o único cadastro do PRD-02 §6.1
ainda sem entrega, e é ele que destrava o caminho.

## What Changes

- **`POST /poderes`**: Admin cadastra poder com nome, descrição, natureza, vigência e papel
  opcional (`RF-02-10`, `RF-01-62`, `RN-01-43`, `RN-01-54`).
- **`GET /poderes`**: a gestão lê o catálogo, paginado, **incluindo o poder desativado**, com
  natureza, vigência e papel legíveis (`RF-02-10`).
- **`PUT /poderes/{id}`**: Admin altera nome, descrição e vigência. A **natureza não entra** —
  mudá-la reescreveria o vínculo já concedido às trilhas.
- **`POST /poderes/{id}/desativacao`**: Admin desativa poder do catálogo.
- **Área Poderes na App 03**: lista distinguindo ativo de inativo, vigente de ciclo futuro e o
  papel declarado; formulário de cadastro; edição; desativação. Com as recusas por papel
  (403), por campo em falta (422) e pelo segundo papel do Território (409).

Nenhuma regra de domínio muda. As quatro conferências que a capacidade já fixa — Admin
exclusivo, natureza que decide se recebe trilha, vigência que nunca trava vínculo e papel
declarado e nunca deduzido do nome — já estão implementadas e permanecem como estão. Esta
fatia abre a porta HTTP e a tela.

### O que fica para depois — e por quê

Nada disto é exclusão nova: o PRD-02 §3.2 mantém o escopo como está, e a fatia apenas não
alcança.

| Adiado                                   | Trava                                                        |
| ---------------------------------------- | ------------------------------------------------------------ |
| Autoria de trilha, missão e atividade    | é a bancada do Mestre na App 09 (PRD-09) — fatia seguinte    |
| `GET /atividades` e o lançamento da aula | dependem da autoria acima (`RF-02-33` a `RF-02-35`, `RF-02-71`) |
| Alterar o papel de um poder já cadastrado| `alterar_poder` não o admite, e nenhum PRD pede a operação   |

### Perguntas ao fundador, antes do `/opsx:apply`

1. **Reativar poder desativado não existe na regra.** `desativar_poder` grava `ativo = False` e
   não há função inversa; nenhum requisito do PRD-02 nem do PRD-01 pede a reativação, ao
   contrário do ponto de apoio, onde `RF-07-47` a previu. Fica de fora por não estar escrita em
   lugar nenhum — se for para existir, é decisão de documento-fonte, não desta change.
2. **O catálogo do Ciclo 01 deve nascer semeado?** `cli.py` já converge chaves e o Admin
   fundador na implantação. Se os poderes do ciclo estão definidos no documento 02 §2, eles
   podem entrar na semeadura em vez de serem digitados um a um — mas o valor de tabela é
   cadastro da gestão, e a decisão é sua. Esta fatia entrega o cadastro pela tela; a semeadura
   só entra se você disser que sim.

## Capabilities

### New Capabilities

Nenhuma. O domínio já está consolidado em `openspec/specs/catalogo-de-poderes/spec.md`.

### Modified Capabilities

- `catalogo-de-poderes`: a leitura do catálogo pela gestão passa a ser requisito — hoje a
  capacidade diz que a distinção entre vigente e ciclo futuro "SHALL ser legível por quem
  consulta o catálogo" sem que exista requisito de consulta. O delta acrescenta a leitura
  paginada da gestão, que inclui o poder desativado, e fixa que a desativação não desfaz o
  vínculo das trilhas já criadas.

## Impact

- **Núcleo**: `backend/src/nucleo/poderes/rotas.py` (novo) e o registro do roteador em
  `principal.py`. Nenhuma migração: `Poder` já existe, com o índice único parcial do papel do
  Território.
- **API**: quatro rotas novas sob `/v1`, com chave de aplicação e credencial de persona.
  `GET /vitrine/poderes` não muda — segue pública e restrita aos poderes ativos.
- **App 03**: `apps/app-03-gestao/src/poderes/` (novo) e a entrada "Poderes" em `App.tsx`.
- **Documentação**: `docs/prds/index.md` registra a quinta fatia do PRD-02. Nenhuma decisão
  nova, nenhum documento-fonte alterado, nenhuma pendência nova no documento 09.

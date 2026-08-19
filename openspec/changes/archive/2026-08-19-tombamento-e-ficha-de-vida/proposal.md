## Why

Nona fatia do **PRD-07 — Economia de recursos e ledger**. Atende `RF-07-11` e `RF-07-48`, e as
regras `RN-07-07`, `RN-07-09` e `RN-07-11`. Reaproveita o `RN-07-10`, já consolidado em
`ponto-de-apoio`.

O acervo permanente é a última frente do documento 05 §3 que o Ciclo 01 opera e que o núcleo
ainda não sustenta. Hoje `duravel` é apenas um rótulo: `aportes/regra.py` a trata igual a
`consumivel`, e nem `reservas/regra.py` nem `catalogo_avulso/regra.py` olham natureza. O efeito
é que os mesmos 46 exemplares da linha Include I podem ser **reservados por uma aula**,
**lastrear um item do catálogo avulso** e — quando o tombamento existir — **ser tombados**: o
mesmo livro contado três vezes. O `RN-07-07` ("credita uma única vez, sem baixa por consumo")
apontava a tensão sem resolvê-la. Esta fatia a resolve e entrega o tombamento e a ficha de
vida.

## What Changes

- **`ItemPatrimonial`** com aporte de origem (opcional), título, número de tombo, ponto de
  apoio e estado de conservação (`RF-07-11`). O **responsável não é campo**: deriva do ponto de
  apoio (`RN-07-10`).
- **Ficha de vida append-only**: quem cuidou do exemplar e as perdas e danos anotados, à imagem
  da imutabilidade que o `Lancamento` já pratica (`RF-07-11`, `RF-07-48`).
- **Perda e dano nunca viram débito** ao Guerreiro(a) nem à família — são anotação da ficha e
  nada mais (`RF-07-48`, `RN-07-09`, documento 05 §3.6). Não há caminho de código que produza
  cobrança a partir de uma anotação.
- **Nenhum empréstimo**: o exemplar não sai do ponto de apoio, e retirada registrada é do ciclo
  seguinte (`RN-07-11`, PRD-07 §3.2).
- **O saldo de natureza `durável` fica inerte** (decisão 1 abaixo): credita Poder Sustentador
  como qualquer outro, e o seu único destino é o tombamento. Duas recusas novas passam a
  guardá-lo — no agendamento da aula e no cadastro do item de catálogo.
- **Teto do tombamento**: os `ItemPatrimonial` de um mesmo aporte não excedem a quantidade
  aportada — o invariante 9 do documento 99 §6 aplicado ao patrimônio. O aporte de origem é
  opcional (`Aporte 0..1`, PRD-07 §8); sem ele não há teto a conferir.

**Quatro decisões novas gravadas no mesmo PR**, antes de virarem comportamento — no
documento-fonte de cada uma e no documento 09:

1. **Patrimônio é paralelo.** O saldo de tipo de natureza `durável` **não é reservável pela
   aula nem serve de lastro ao catálogo avulso**. Fonte: documento 04 §1 (saldo e lastro).
2. **O número de tombo é digitado pelo Admin**, não gerado pelo núcleo, e é **único por ponto
   de apoio**. Fonte: documento 05 §3.
3. **Item de catálogo avulso de tipo durável é recusado no cadastro.** O documento 02 §8.2 diz
   "item sem lastro fica inativo, nunca é recusado" — regra escrita para o lastro transitório
   que ainda vai chegar. O tipo durável é impossibilidade estrutural, não lacuna transitória, e
   a frase da fonte ganha a ressalva. Fonte: documento 02 §8.2.
4. **O responsável do exemplar deriva do ponto de apoio**, não é campo próprio. O PRD-07 §8 o
   lista entre os atributos do `ItemPatrimonial`, mas o documento 05 §3.4 designa **uma** pessoa
   por ponto de apoio, que "consta do inventário" e cuja responsabilidade sobrevive à troca de
   turma e de Mestre. Por fonte única o documento 05 vence, e o §8 do PRD-07 se corrige.

**Consequência de cadastro**, registrada aqui porque a decisão 1 a torna vinculante — é
cadastro da gestão, não código: **"livro" passa a ser dois tipos de recurso distintos**. O
livro da linha Alpha é **consumível**, porque é doado e a baixa definitiva precisa de saldo
vivo; o da linha Include I é **durável**, acervo permanente que tomba. A camisa é consumível
pelo mesmo motivo; o kit em MDF o documento 05 §C já declara consumível na fonte.

## Capabilities

### New Capabilities

- `patrimonio`: o exemplar tombado e a sua ficha de vida — o tombamento com teto no aporte, o
  tombo único por ponto de apoio, o responsável derivado, a anotação de perda e dano que nunca
  vira débito, e a regra que mantém o saldo durável inerte.

### Modified Capabilities

- `reserva-de-recurso`: a reserva passa a **recusar tipo de natureza durável**. Os requisitos de
  hoje descrevem a reserva sem distinguir natureza alguma.
- `catalogo-avulso`: o cadastro passa a **recusar item de tipo durável**. O requisito de hoje diz
  que o item sem lastro nasce inativo e nunca é recusado; a impossibilidade estrutural passa a
  ser exceção declarada.

## Impact

- **Código**: nasce `backend/src/nucleo/patrimonio/`. `backend/src/nucleo/reservas/` e
  `backend/src/nucleo/catalogo_avulso/` ganham a recusa por natureza. Migração Alembic para as
  tabelas do item e da ficha de vida.
- **API**: `POST /v1/itens-patrimoniais` (Admin tomba), `GET /v1/itens-patrimoniais` (gestão,
  filtrada por comunidade) e a rota de anotação da ficha de vida. Nenhuma rota pública nova.
  A §9 do PRD-07 não lista rota de patrimônio alguma, e o PRD-09 §522 já as pressupõe como sendo
  do PRD-07 — nomeá-las é parte desta fatia, como `/aulas/{id}/trocas` foi na oitava.
- **Depende de**: `ponto-de-apoio`, `aporte`, `catalogo-de-tipos-de-recurso`,
  `reserva-de-recurso`, `catalogo-avulso` e `persona-e-credencial` — todos já consolidados.
- **Risco de regressão baixo**: nenhum teste da suíte usa `duravel` hoje (zero ocorrências em
  `backend/tests/`), e as duas recusas novas incidem sobre um caminho que nenhum teste exercita.
- **Documentação**: documentos 02 §8.2, 04 §1 e 05 §3 (fontes das quatro decisões), documento 09,
  PRD-07 §§8, 9 e 13, e `docs/prds/index.md` pela situação do PRD-07. Nenhum arquivo novo em
  `docs/`, logo a `nav` do `mkdocs.yml` não muda.

## Fora do escopo

Reproduz o que o PRD-07 §3.2 já exclui, mais o recorte desta fatia:

- **Empréstimo de bancada e reposição solidária**: o documento 05 §3 os adia para o ciclo
  seguinte, e o PRD-07 §3.2 os repete. No Ciclo 01 a perda é anotada na ficha de vida.
- **Conferência de inventário** — `RF-07-20`, único "desejável" do PRD-07: trava em "a cada
  **módulo**", e "módulo" não é definido em documento algum. Fatia própria quando tiver dono.
- **Baixa definitiva de recompensa entregue** — `RF-07-13`, `RN-07-08`, `RN-07-14`: depende de
  `RecompensaDeMarco`, **entidade nova do PRD-09** (§8 daquele PRD), que traz o marco, o lastro
  confirmado e a situação da entrega. Não nasce aqui.
- **Desafio extra** — `RF-07-15`, `RF-07-39`, `RF-07-40`, `RF-07-41`: travado enquanto não
  existir `DesafioExtra`, que nasce em PRD-09 ou PRD-14.
- **Produção executiva** — `RN-07-32` (frente e período apurado do aporte): resto pequeno, fatia
  própria.
- **Ficha de vida lida pelo Guerreiro(a)** — `RF-05-48` e `GET /v1/eu/acervo`: são do PRD-05
  (App 05).
- **Interface de tombamento e inventário**: App 03 (PRD-02, `RF-02-52` a `RF-02-56`).
- **Badge "Guardião do Acervo"**: documento 05 §3.3, fora do recorte do patrimônio no PRD-07.

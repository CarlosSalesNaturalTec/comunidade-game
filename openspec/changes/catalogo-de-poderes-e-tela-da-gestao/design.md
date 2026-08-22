## Context

O domínio já está consolidado em `openspec/specs/catalogo-de-poderes/spec.md`, e a regra já
está escrita em `backend/src/nucleo/poderes/regra.py` — `cadastrar_poder`, `alterar_poder`,
`desativar_poder` e `buscar_poder_do_territorio`, com o índice único parcial
`uq_poder_papel_territorio` no modelo. Falta a porta HTTP e a tela. Motivação em
`proposal.md` — Why.

## Goals / Non-Goals

**Goals:**

- Expor as três escritas e a leitura da gestão sem tocar `poderes/regra.py`.
- Entregar a área Poderes na App 03 no mesmo padrão de `pontos-de-apoio/`.

**Non-Goals:**

- Alterar qualquer conferência já implementada, inclusive a pré-conferência de 409 do papel do
  Território.
- Tocar `GET /vitrine/poderes`, que segue pública e restrita aos poderes ativos.
- Semear o catálogo na implantação — é a pergunta 2 da `proposal.md`.

## Decisions

- **A desativação é rota própria, `POST /poderes/{id}/desativacao`**, e não um campo do `PUT`
  nem um `DELETE`. Espelha `pontos-de-apoio` e `chaves`, mantém a leitura do log de auditoria
  legível por rota e deixa claro que o poder não é apagado. Descartados: `DELETE`, que
  sugeriria remoção; `ativo` no corpo do `PUT`, que misturaria edição de rótulo com mudança de
  situação.
- **O `PUT` recebe só nome, descrição e vigência.** É o que `alterar_poder` admite; natureza e
  papel ficam fora do corpo, e não há caminho de código que os altere. Descartado: aceitar os
  campos e ignorá-los, que esconde a recusa do cliente.
- **`GET /poderes` pagina por `(nome, id)`** no contrato único de listagem, com o cursor
  codificado como nas demais listagens. Descartado: ordenar por data de criação, que
  embaralharia o catálogo a cada cadastro novo.
- **`GET /poderes` não aceita filtro por comunidade.** O poder é bem comum da plataforma e
  `Poder` não tem coluna de comunidade — o `RF-01-18` não o alcança, como já vale para a
  `Trilha` (`RN-01-42`). Exige persona em sessão, sem restringir por papel: a gestão inteira lê
  o catálogo, e só a escrita é de Admin.
- **A tela reaproveita a camada visual comum.** `apps/app-03-gestao/src/poderes/`, com
  `TelaDePoderes`, `ListaDePoderes`, `FormularioDePoder` e `DesativarPoder`, sobre os tokens
  de `comum/`. A entrada "Poderes" entra em `App.tsx` ao lado de "Comunidades", por ser
  cadastro de catálogo. Descartado: pendurar o catálogo dentro da área Comunidades, que
  confundiria bem comum com dado de comunidade.

## Risks / Trade-offs

- **Poder cadastrado com natureza errada não tem conserto pela API** → é decisão já tomada em
  `alterar_poder`, e o catálogo do Ciclo 01 é pequeno; a tela deixa a natureza explícita no
  formulário, com o aviso de que ela não muda depois.
- **Sem semeadura, uma implantação nova nasce sem o poder do Território e a coleta recusa com
  409** → é o comportamento que `RN-08-15` já fixa, e a tela desta fatia é justamente o caminho
  para resolvê-lo; a pergunta 2 da `proposal.md` decide se vale automatizar.

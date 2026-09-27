# Tasks

## 1. Cliente da rota

- [x] 1.1 (`RF-09-122`) Em `apps/app-09-mestre/src/responsaveis/api.ts`, declarar
      `listarResponsaveis` e os tipos da saída de `GET /v1/responsaveis`, que o núcleo já
      serve. Verificável: o tipo cobre `nome` e `vinculados` com `nick` e `grau_de_parentesco`,
      e nada de credencial ou contato.

## 2. Tela da área

- [x] 2.1 (`RF-09-122`, `RF-09-62`) Separar a `TelaDeResponsaveis` atual em
      `FormularioDeResponsavel` — o fluxo de cadastro, vínculo e credencial como está, com
      `rotuloDoVinculo` junto — e uma `TelaDeResponsaveis` nova que assume a área, com
      `Cabecalho` e `Moldura` (design — decisões 1 e 3). Verificável: `App.tsx` segue montando
      `TelaDeResponsaveis` e a página não ganha moldura dupla.
- [x] 2.2 (`RF-09-122`) Criar a lista no padrão de `ListaDeResponsaveis` da App 03, com
      `Tabela` de `comum/react`, sinalizando o responsável sem vínculo e o Guerreiro(a) sem
      nick (design — decisão 4). Verificável: a área abre na lista, não no cadastro.
- [x] 2.3 (`RF-09-122`, `RF-09-63`, `RN-09-15`) Fazer o formulário aceitar um responsável já
      existente e ligar a retomada à linha da lista (design — decisão 2), mantendo a mensagem
      do teto de três. Verificável: vincular um segundo Guerreiro(a) a um responsável antigo
      não cadastra responsável novo.

## 3. Testes da App 09

- [x] 3.1 (`RF-09-122`) Em `apps/app-09-mestre/src/responsaveis/responsaveis.test.tsx`, cobrir
      os sete cenários do delta: a área abre na lista; cadastro interrompido sinalizado; o
      cadastro alcançável a partir da lista; a retomada cria o vínculo sem cadastrar; o teto de
      três na retomada; lista vazia dita; a lista não expõe credencial nem dado civil. Ajustar
      os testes existentes do cadastro, do vínculo e da credencial ao novo ponto de entrada da
      área. Verificável: `vitest run` da App 09 verde, com os testes anteriores preservados.

## 4. Documentação

- [x] 4.1 Marcar a fatia 22 do PRD-09 como implementada em
      `openspec/cronograma-de-fatias.md`. Nada muda em `docs/`: `RF-09-122` já foi declarado no
      PRD-09, a decisão já está nos documentos 02 §1 e 09 §1, e o documento 99 §8 já registra a
      dependência do PRD-09 no PRD-02 — tudo entregue pela fatia 24 do PRD-02.

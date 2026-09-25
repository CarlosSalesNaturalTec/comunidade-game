# Tasks

## 1. Os quatro componentes em `comum/react`

- [ ] 1.1 Criar a **carta do personagem** com os valores do documento 15 §8.1 — superfície, borda de
      1 px, raio lido do token do temperamento, avatar em círculo com metade da largura, nick na
      família de destaque —, recebendo de quem a monta o que a variante exibe (design — decisões 1 e
      6).
- [ ] 1.2 Recusar a montagem **incompleta**: variante sem o que o documento 11 §8.2 exige não é
      apresentada como carta (design — decisão 2).
- [ ] 1.3 Criar o **emblema de nível contável** do §8.2 — marcas iguais ao nível, moldura fechada no
      5, nome do poder na moldura, sempre de trilha ou poder —, ao lado do numeral (design — decisão
      4).
- [ ] 1.4 Desenhar as **seis silhuetas de badge** do §8.3, legíveis a `24` px sem depender de cor
      (design — decisão 3).
- [ ] 1.5 Criar o **glifo de poder** do §8.4 sobre o sistema de ícone da fatia do temperamento
      Arena, com um glifo por poder do catálogo e o **genérico** para o poder sem glifo (design —
      decisão 5).
- [ ] 1.6 Exportar os quatro em `comum/react/indice.ts` e conferir `comum/package.json`.
- [ ] 1.7 Cobrir, em teste do `comum`, os onze cenários do delta de `camada-visual-comum`.

## 2. A Área do Guerreiro(a) usa a carta e o emblema

- [ ] 2.1 Em `apps/app-05-guerreiro/src/carteira/MinhaCarteira.tsx`, apresentar a **carta do próprio
      Guerreiro(a)**, montada das leituras que a Área já consome, com o avatar desenhado e o padrão
      do projeto quando faltar (`RF-05-50`, `RF-05-51`, design — decisão 1).
- [ ] 2.2 Em `apps/app-05-guerreiro/src/trilha/Progresso.tsx`, apresentar o nível pelo emblema
      contável e os badges pela silhueta da família com o glifo do poder, mantendo o numeral
      (`RF-05-15`, `RF-05-16`, design — decisão 4).
- [ ] 2.3 Conferir que nada de vedado pelo documento 11 §8.2 entra na carta — imagem real, nome
      civil, rede social, canal de contato (invariantes 9 e 10).

## 3. Testes

- [ ] 3.1 Em teste da App 05, cobrir os três cenários da carta do Guerreiro(a): vê a própria carta,
      a carta não expõe o vedado, e sem avatar usa o padrão do projeto (`RF-05-50`, `RF-05-51`).
- [ ] 3.2 Em teste do progresso da App 05, cobrir "O nível aparece como marcas contáveis" e "O badge
      aparece pela silhueta da família", com os cenários que já existiam seguindo válidos
      (`RF-05-15`, `RF-05-16`).

## 4. Documentação

- [ ] 4.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md` e
      **corrigir o recorte previsto** nela: a fatia não aplica carta nas telas de equipe (design —
      decisão 2).
- [ ] 4.2 Registrar no documento 09 §1 a pendência das duas famílias de badge que o documento 15
      §8.3 declara e o `TipoDeBadge` do núcleo não tem — **de conquista** e **de território**
      (design — decisão 3). O documento 15 e o documento 11 **não** mudam: a change os cumpre. Nada
      muda em `docs/prds/index.md`, no documento 99 nem na `nav` do `mkdocs.yml`.

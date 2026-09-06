## 1. Tabela das personas

- [ ] 1.1 `ListaDeAdultos.tsx` passa a `Tabela`, com as colunas nome, e-mail, nick e
      artefatos, e a linha acionável que abre a ficha; o nick vazio ocupa a própria célula, com
      o aviso de que a pessoa não aparece em superfície pública (`RF-02-01`, `RN-14-10`,
      design — decisão 2).
- [ ] 1.2 `ListaDeGuerreiros.tsx` passa a `Tabela` com as colunas que ela já traz — nick,
      avatar, comunidade e início do vínculo (`RF-02-01`, `RF-02-15`, design — decisão 4).

## 2. Ficha do adulto

- [ ] 2.1 `FichaDoAdulto.tsx` sobre o `Dialogo`: nome, e-mail, WhatsApp, nick e os artefatos
      comprobatórios, cada um com rótulo e o endereço como link alcançável (`RF-02-02`,
      `RF-02-03`, `RF-02-04`, `RN-02-01`, design — decisões 1 e 3).
- [ ] 2.2 A ficha oferece o caminho de gravar o nick quando ele está vazio, reaproveitando
      `FormularioDeNick` sem mudar a regra dele — nenhum nick é sugerido (`RF-02-01`,
      `RN-01-30`, `RN-14-10`).
- [ ] 2.3 `TelaDeAdultos.tsx` liga a linha da tabela à ficha e recarrega a lista quando o nick
      é gravado.

## 3. Forma que faltava

- [ ] 3.1 `index.css`: dar forma a `.cg-campo-de-artefato`, hoje usada sem definição, e apagar
      `.lista-de-personas` e as suas variações, que a tabela substitui.

## 4. Testes

- [ ] 4.1 `personas.test.tsx`: a tabela de Mestres lista os cadastrados; a ficha de um Mestre
      mostra os artefatos com rótulo e endereço; adulto sem artefato nenhum mostra a ficha sem
      lista, e não uma ficha quebrada; o nick vazio aparece na coluna e a ficha oferece gravá-lo;
      a tabela de Guerreiros e Guerreiras traz nick e vínculo (cenários da spec desta change).

## 5. Documentação

- [ ] 5.1 Marcar a fatia 18 como implementada em `openspec/cronograma-de-fatias.md` e mover
      para *Já decididos*, no documento 09 §1, a decisão do fundador de 2026-09-06 sobre o que
      esta fatia deixa de fora. Nenhum documento-fonte e nenhum PRD mudam — a fatia não cria
      regra —, nenhum arquivo novo entra em `docs/`, e a situação do PRD-02 em
      `docs/prds/index.md` não muda, porque a fatia 16 segue em aberto.

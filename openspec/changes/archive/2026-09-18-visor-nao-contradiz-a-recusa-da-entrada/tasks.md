## 1. A tela de entrada

- [x] 1.1 Em `TelaDeEntradaDoGuerreiro`, condicionar o retorno do laço ao momento da captura,
      como `TelaDeCaptura` e `TelaDeMedicaoDoLimiar` já fazem: o `Visor` recebe o estado do laço
      enquanto a tentativa corre e `null` a partir do desfecho, qualquer que seja ele — falha de
      preparo, vivacidade reprovada, recusa do núcleo, erro de rede ou presença já registrada
      (`RF-04-64`, `RN-04-34`, design — decisão 1).
- [x] 1.2 Conferir que a frase única da recusa e a frase distinta da falha de preparo seguem
      como estão, sem novo texto e sem revelar a causa (`RF-04-20`, `RF-04-65`, `RN-01-22`,
      design — decisão 2).

## 2. Testes

- [x] 2.1 Em `entrada.test.tsx`, cobrir os dois cenários novos do delta: vivacidade confirmada
      seguida de recusa do núcleo apresenta **só** a frase da recusa; e tentativa encerrada por
      falha de preparo ou por vivacidade reprovada apresenta só a frase daquele desfecho. Cobrir
      também que o visor aparece durante a captura, que é o cenário já vigente e não pode
      regredir (`RF-04-64`, `RF-04-20`, `RF-04-65`, `RN-04-34`).

## 3. Documentação

- [x] 3.1 Acrescentar ao bloco do PRD-04 do `openspec/cronograma-de-fatias.md` a linha desta
      change, **sem número de fatia** — correção de defeito preexistente, no molde da linha de
      `2026-09-17-correcao-de-aulas-canceladas-e-modelos-de-biometria`. Nenhuma decisão nova
      foi tomada, nenhum requisito mudou e nenhum arquivo entrou em `docs/`: os documentos 03,
      09 e 99, o PRD-04, o `docs/prds/index.md` e a `nav` do `mkdocs.yml` seguem como estão.

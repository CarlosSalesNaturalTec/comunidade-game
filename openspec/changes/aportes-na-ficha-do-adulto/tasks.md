# Tasks

## 1. Leitura no núcleo

- [ ] 1.1 Em `backend/src/nucleo/poder_sustentador/rotas.py`, criar
      `GET /provedores/{provedor_id}/aportes` restrita ao Admin (403 antes de consultar; 404
      indistinto para inexistente, Guerreiro(a) e responsável). A resposta traz os aportes
      homologados, do mais recente ao mais antigo, com nome e unidade do tipo, ponto de
      apoio, moedas, `valor_de_origem`, forma, destinação e `tem_comprovante`; traz também o
      Poder Sustentador por `poder_sustentador_de` e as declarações `pendente` com data, valor
      declarado e origem da escolha. Nada de comprovante, referência nem dado bancário
      (`RF-02-117`, `RN-02-34`, `RN-07-06`, `RN-07-22`, `RN-14-07`). Verificar: os testes de
      1.2.
- [ ] 1.2 Criar `backend/tests/test_aportes_do_provedor_rota.py` com os cenários da spec
      `poder-sustentador`:
      - Admin lê dois aportes em ordem;
      - reais ao Admin;
      - comprovante só como marca;
      - pendente separada, recusada fora, pendente fora do Poder Sustentador;
      - Mestre com absorção;
      - Mestre e Apoiador recusados;
      - 404 para Guerreiro(a) e para inexistente.

      Acrescentar, no teste existente de `GET /meus-aportes` e no da leitura pública, a
      asserção de que seguem sem reais (`RF-02-117`, `RN-02-34`, `RN-07-05`, `RF-07-17`).
      Verificar: `uv run pytest` dos arquivos tocados passa.

## 2. Ficha do adulto na App 03

- [ ] 2.1 Em `apps/app-03-gestao/src/personas/api.ts`, criar `lerAportesDoProvedor(id, token)`
      e os tipos da resposta (`RF-02-117`). Verificar: o tipo compila.
- [ ] 2.2 Mover `formatarMoedas` e `formatarQuantidade` de `recursos/formatacao.ts` para um
      lugar comum dentro da App 03, ou importá-los de lá, sem duplicar (`RF-02-117`).
      Verificar: os testes de Recursos seguem verdes.
- [ ] 2.3 Em `apps/app-03-gestao/src/personas/FichaDoAdulto.tsx`, criar a seção **Aportes**,
      que busca ao abrir:
      - o Poder Sustentador;
      - a tabela dos homologados em pt-BR, com os reais em BRL ao lado das moedas quando
        houver;
      - a marca de comprovante;
      - a lista das declarações pendentes à parte;
      - os estados de carregando, de erro e de "ainda não há aporte".

      Nenhuma ação de baixar, editar, estornar, homologar ou recusar (`RF-02-117`,
      `RN-02-34`, `RN-02-01`). Verificar: os testes de 2.4.
- [ ] 2.4 Em `apps/app-03-gestao/src/personas/personas.test.tsx`, cobrir os cenários da spec
      `aplicacao-de-gestao`:
      - aporte com moedas e comprovante;
      - reais ao lado das moedas;
      - pendente à parte, sem ação;
      - ficha sem aporte, com zero e aviso;
      - nenhum controle de edição.

      Ajustar os testes da ficha que já existem para a chamada nova (`RF-02-117`,
      `RN-02-34`). Verificar: `vitest run` de personas passa.

## 3. Documentação

- [ ] 3.1 Documento 04 §1, "Reais aparecem só onde se paga": acrescentar em uma frase a
      exceção da ficha do adulto na gestão, só do Admin e sempre ao lado das moedas. No
      documento 99 §6, ajustar o invariante 16 na mesma medida. No documento 09 §1, "Já
      decididos", acrescentar a linha "Aportes na ficha do adulto", com a decisão de
      2026-11-17 (`RN-02-34`). Verificar: o invariante 16 e o documento 04 dizem a mesma
      coisa.
- [ ] 3.2 Revisar o PRD-02:
      - `RF-02-117` na §6.1;
      - `RN-02-34` na §7;
      - a rota na tabela da §9;
      - a linha na §13;
      - os dois identificadores na §15.

      Em `openspec/cronograma-de-fatias.md`, criar a fatia 29 do PRD-02 com o slug e marcá-la
      `implementado` ao fechar. `docs/prds/index.md` não muda, porque o PRD-02 já está
      implementado. Nenhum arquivo novo em `docs/`, então a `nav` não muda (`RF-02-117`,
      `RN-02-34`). Verificar: `mkdocs build --strict` e `npm run lint` passam.

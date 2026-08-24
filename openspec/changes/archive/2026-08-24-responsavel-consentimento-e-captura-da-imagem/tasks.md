## 1. Núcleo — o responsável ganha nome e a matriz ganha o testemunho

- [x] 1.1 `responsaveis/regra.py` e `responsaveis/rotas.py`: `cadastrar_responsavel` passa a
      exigir o `nome`, recusando em branco com 422, e a repassá-lo a `criar_persona`, que já o
      aceita. `POST /v1/responsaveis` recebe o corpo com o nome (`RF-04-60`, `RF-01-13`).
      Verificação: a rota devolve 201 com nome gravado e 422 sem ele.
- [x] 1.2 `permissoes.py`: operação de escrita nova do Mestre para o **registro do termo impresso
      testemunhado**, distinta de `Operacao.consentimentos`, que é do responsável (design —
      decisão 3). Verificação: o teste da matriz mostra Mestre e Admin com a operação e
      responsável sem ela.
- [x] 1.3 `configuracao.py`: constante da **versão vigente do termo de consentimento**, no padrão
      de `ciclo_rotulo`, com o valor inicial `2026-08` (design — decisão 2). Verificação: a
      configuração carrega o valor e o teste da rota o encontra no registro gravado.

## 2. Núcleo — a porta do consentimento

- [x] 2.1 `consentimentos/rotas.py` (novo): `POST /v1/consentimentos` sob a operação da tarefa
      1.2, recebendo responsável, Guerreiro(a), tipo, decisão, origem e testemunha, carimbando a
      versão da configuração e devolvendo identificador e momento. `consentimentos/regra.py` não
      muda (`RF-01-19`, `RF-04-12`, `RN-01-12`). Verificação: 201 no caminho feliz, 403 para papel
      sem a operação, 422 para tipo fora do conjunto e recusa quando não há vínculo vigente.
- [x] 2.2 `principal.py`: registrar o roteador de consentimentos sob `/v1`. Verificação: a rota
      aparece no OpenAPI e responde fora de 404.

## 3. App 01 — a fronteira da Human

- [x] 3.1 `package.json` da App 01: dependência da Human, com os modelos carregados **sob
      demanda** e não na subida (design — decisão 5, documento 03 §§3.3, 3.4). Verificação:
      `vitest run` da App 01 continua passando sem baixar modelo.
- [x] 3.2 Módulo único de biometria da App 01, expondo provar vivacidade e gerar descritor, e
      sendo o único lugar que importa a Human, carrega modelo ou toca `getUserMedia`. Devolve
      `number[]`; a fotografia não sai dele (`RF-04-14`, `RF-04-48`, `RN-04-08`, `RN-04-12`).
      Verificação: teste com o módulo substituído; nenhuma imagem em corpo de requisição.
- [x] 3.3 Clientes de API da App 01 para responsável, vínculo, consentimento e descritor, no
      desenho de `api/guerreiros.ts` (`RF-04-12`, `RF-04-13`, `RF-04-60`). Verificação: teste de
      cada cliente contra o contrato da §9 do PRD-04 — via os componentes que os chamam, mesmo
      precedente de `api/guerreiros.ts`/`onboarding.test.tsx`.

## 4. App 01 — o fluxo da jornada 5.2

- [x] 4.1 Tela do responsável no onboarding: nome e grau de parentesco, encadeada depois do
      cadastro do Guerreiro(a), sem pedir e-mail, senha ou documento (`RF-04-60`). Verificação:
      recusa sem grau de parentesco; nenhuma tela pede e-mail.
- [x] 4.2 Tela do termo e confirmação da assinatura pelo Mestre ou Admin como testemunha, antes
      de qualquer captura (`RF-04-11`, `RF-04-12`, `RN-04-07`). Verificação: a câmera não abre
      enquanto a confirmação não é dada.
- [x] 4.3 Tela de captura: vivacidade, descritor e envio, com a recusa de captura sem
      consentimento explicada em linguagem simples (`RF-04-13`, `RF-04-48`). Verificação:
      vivacidade reprovada não envia nada e oferece nova tentativa.
- [x] 4.4 Detecção de câmera: sem ela, o onboarding **continua** pelo caminho sem imagem, com
      aviso de que a captura exige outro aparelho (`RF-04-04`, `RF-04-15`, `RN-04-03`,
      `RN-04-09`, design — decisão 6). Verificação: aparelho sem câmera conclui o cadastro ativo
      e sem imagem.
- [x] 4.5 Retomada por passo concluído: o atendimento guarda `guerreiro_id` e `responsavel_id` e
      recomeça do primeiro passo que faltou, sem repetir o que já gravou (design — decisão 4).
      Verificação: falha simulada em cada elo da cadeia deixa o estado da tabela do design, e
      nenhum cadastro fica pela metade.

## 5. Testes

- [x] 5.1 `tests/test_consentimento_rota.py` (novo): os cenários da spec `consentimento` —
      registro com testemunha e fuso, 403 por papel, 422 por tipo, recusa sem vínculo, versão
      vinda da configuração e não do corpo, versão trocada que não reescreve o passado. A
      biometria que não nasce da autorização de divulgação já está coberta em
      `test_consentimento.py`, ao nível da regra.
- [x] 5.2 `tests/test_responsavel_rota.py` e `tests/test_auditoria_middleware.py`: os cenários
      novos da spec `responsavel-e-vinculo` — nome gravado, 422 sem nome, e nenhuma credencial
      nascendo com o cadastro.
- [x] 5.3 Testes da App 01 para os cenários novos da spec `aplicacao-da-aula-presencial`: o
      responsável e o grau de parentesco, o termo antes da câmera, a testemunha registrada, a
      vivacidade reprovada, a ausência de imagem em requisição e em registro de erro, o aparelho
      sem câmera e a retomada por passo. Inclui os critérios da §12 do PRD-04 tal como corrigidos
      na tarefa 6.2.

## 6. Documentação

- [x] 6.1 Documento 09 §1: mover para "Já decididos" as três decisões do fundador de 2026-08-24 —
      o **nome** como conteúdo do responsável mínimo, a **versão do termo carimbada pelo núcleo**
      e a **falta de câmera que fecha só a captura**.
- [x] 6.2 PRDs afetados pelas decisões: matriz do **PRD-01 §4** ganha a operação do testemunho;
      **PRD-04 §6.1** corrige o `RF-04-04`, **§7** o `RN-04-03`, e **§12** os dois critérios que
      o design — decisão 6 identifica (o bloqueio por falta de câmera e a vivacidade atribuída ao
      núcleo, que o documento 03 §3.3 põe no aparelho e no contexto presencial).
- [x] 6.3 `docs/prds/index.md`: a narrativa da terceira fatia do PRD-04, dizendo o que ficou
      pendente — `RF-04-16` e `RF-04-18`, e a leitura do termo em voz alta. Nenhum arquivo novo
      em `docs/`, logo a `nav` do `mkdocs.yml` não muda; a relação entre documentos não muda,
      logo o documento 99 não muda.

# Tasks

A ordem dos grupos é a ordem das camadas do `design.md` — decisão 6. Nenhum grupo de código
começa antes de o documento-fonte dele estar escrito.

## 1. Medição da cor, antes de qualquer edição

- [ ] 1.1 Medir as duas razões de contraste do par verde — `cal-000` sobre `sucesso-600` no
      claro e `sucesso-400` com `tinta-900` no escuro — e verificar que **as duas** passam o
      piso de 4,5:1 do documento 15 §3.3. Se alguma não passar, **parar a change** e levar ao
      fundador: nenhum degrau se inventa para salvar o desenho (design — decisão 1).

## 2. Documentos-fonte (nível 1)

- [ ] 2.1 Documento 03 §8: tirar o poder das três listas — seções apresentadas, "cada card abre
      a página individual do personagem" e a chamada em toda página individual —, tirar
      "Como apoiar" das seções públicas registrando que ela **segue gravável no núcleo**, e
      trocar o rótulo da chamada para "Quero apoiar". Verificar que a §8 não cita mais seção de
      poder nem tela de "Como apoiar", e que a linha do "Entrar" segue como está.
- [ ] 2.2 Documento 15 §3.2: acrescentar **uma frase** — a família Sucesso serve também o
      "Entrar" do herói, e o token significa "deu certo" e "entre aqui". §3.3: acrescentar as
      duas linhas com os valores **medidos** na tarefa 1.1. Verificar que nenhuma família nova
      e nenhum degrau novo entraram na tabela da §3.2.
- [ ] 2.3 Documentos 02 §1, 08, 12 §4 e 14 §10: trocar o rótulo nas menções à chamada, **uma
      frase cada**, sem repetir a regra do documento 03. Verificar por busca que nenhuma menção
      a "Quero participar" restou em `docs/` fora do histórico de decisões do documento 09.
- [ ] 2.4 Documento 09 §1: mover as **seis decisões** de 2026-10-11 para "Já decididos" — a
      ordem da abertura, a saída da seção de poderes, a saída da tela de "Como apoiar", a
      seção própria das necessidades, o rótulo da chamada com o caminho preservado, e o verde
      reaproveitando a família Sucesso. Verificar que cada linha aponta o documento-fonte que a
      grava e que nenhuma pendência nova nasceu sem entrar na tabela.

## 3. PRDs (nível 2)

- [ ] 3.1 PRD-03: `RF-03-02` passa a **cinco** seções com cards (sem poderes); `RF-03-39` passa
      a nomear "Quero apoiar" e deixa de ser parcial, porque o poder não tem mais página
      individual; `RF-03-45` e `RF-03-46` passam a dizer que "Como apoiar" não tem tela pública
      e que a chave PIX fica na porta. Ajustar as §§2, 5.9 e 6.4 ao que os requisitos passaram a
      dizer. Verificar que a §2 lista cinco seções e que nenhuma seção do PRD cita tela de
      "Como apoiar".
- [ ] 3.2 PRD-02 §16: registrar que a tela de edição do institucional segue valendo para as
      três seções, uma das quais — "Como apoiar" — **não tem mais tela pública** (`RF-02-80`).
      Verificar que nenhum requisito do PRD-02 foi retirado: só o alcance público mudou.

## 4. A cor do "Entrar"

- [ ] 4.1 `comum/tokens.css`: acrescentar `--cor-sobre-sucesso` nos **dois** modos — `cal-000`
      no claro, `tinta-900` no escuro —, ao lado dos `--cor-sobre-*` que já existem. Verificar
      que nenhuma primitiva nova entrou: o token aponta para primitiva já declarada
      (design — decisão 1).
- [ ] 4.2 `apps/app-06-vitrine/src/index.css`: renomear `.cg-botao--marca` para
      `.cg-botao--entrada` e repintá-la com `--cor-sucesso` no fundo e no contorno e
      `--cor-sobre-sucesso` no texto, com o comentário que registra **por que o contorno reusa
      o 600** — a família não tem 700, e a regra do 700 é de ficha, não de botão. Atualizar
      `src/abertura/EntradaDaAbertura.tsx` para a classe nova e verificar por busca que
      `cg-botao--marca` não restou em nenhum arquivo (`RF-03-58`, design — decisões 1 e 3).
- [ ] 4.3 `src/testes/entrada.test.tsx` e `src/testes/heroi.test.tsx`: cobrir o cenário
      "As duas ações se leem como um par de iguais" do delta — o par lado a lado, de mesma
      altura, forma e peso, cada ação reconhecível pelo próprio rótulo e **sem depender da
      cor** —, e o cenário "O 'Entrar' do herói é o único da tela" seguindo verde.

## 5. As duas seções que saem, e a ordem da abertura

- [ ] 5.1 Apagar `src/poderes/SecaoDePoderes.tsx`, a função `listarPoderes` de
      `src/api/leituras.ts` e o tipo `PoderPublico` se nada mais o usar. Verificar por busca
      que a vitrine não consome mais `/v1/vitrine/poderes` e que **nenhum arquivo de
      `backend/` foi tocado** — a rota fica (`RF-03-02`, design — decisão 4).
- [ ] 5.2 `src/pages/index.astro`: tirar a seção de poderes e a de "Como apoiar", promover
      `NecessidadesEmAberto` a seção própria com o título "Necessidades em aberto", e deixar a
      ordem em Ranking, Portfólio de criações originais, Guerreiros e Guerreiras, Apoiadores,
      Necessidades em aberto, Mestres, Comunidades Virtuais, Construir sobre a API, Quem somos,
      Contatos. Verificar que `comoApoiar` deixou de ser buscado no build e que `quemSomos` e
      `contatos` seguem (`RF-03-45`, `RF-03-47`).
- [ ] 5.3 `src/testes/portfolioRankingEPoderes.test.tsx` e `src/testes/arena.test.tsx`: retirar
      os casos da seção de poderes e cobrir os cenários acrescentados "A abertura não traz seção
      de poderes" e "O poder segue aparecendo no Guerreiro(a)" (`RF-03-02`, `RF-03-05`).
- [ ] 5.4 `src/testes/necessidadesEmAberto.test.tsx`: cobrir os cenários "A seção aparece por si
      na abertura" e "Sem necessidade em aberto, a seção diz isso", e o cenário "Nenhuma tela
      pública apresenta 'Como apoiar'" percorrendo a abertura inteira (`RF-03-47`, `RF-03-45`).

## 6. O rótulo da chamada, nos três lugares

- [ ] 6.1 Trocar o rótulo para "Quero apoiar" em `src/abertura/Heroi.tsx` (o link do herói),
      `src/convite/ChamadaDeParticipacao.tsx` (a chamada ao pé das páginas individuais) e
      `src/convite/PortaDoConvite.tsx` (o título da porta), e atualizar os comentários dos três
      que nomeiam o rótulo antigo. Verificar que `CAMINHO_DO_CONVITE` **não mudou** e que
      `src/pages/quero-participar.astro` segue no mesmo endereço (`RF-03-39`, `RF-03-42`).
- [ ] 6.2 `src/convite/PortaDoConvite.tsx`: conferir que a porta segue oferecendo a chave PIX e
      as necessidades, agora como **único** lugar público da chave, e que o garfo das sete
      modalidades continua inteiro, a pretensão de ensinar incluída (`RF-03-43`, `RF-03-46`,
      documento 14 §10).
- [ ] 6.3 `src/testes/convite.test.tsx`: trocar as asserções de rótulo e cobrir os cenários
      "Acompanhar chega à porta do convite", "O endereço da porta não mudou com o rótulo",
      "Quem não quer se cadastrar encontra o PIX" e "A chave PIX continua alcançável pelo
      visitante" (`RF-03-39`, `RF-03-40`, `RF-03-42`, `RF-03-43`).
- [ ] 6.4 `src/testes/TelaDaVitrine.tsx`, `src/testes/cardsEPagina.test.tsx` e
      `src/testes/mestresEApoiadores.test.tsx`: alinhar a composição de teste e as asserções de
      rótulo das quatro páginas individuais aos cenários "A página do Guerreiro(a) convida", "A
      página da comunidade convida", "A página do Mestre convida" e "A página do Apoiador
      convida" (`RF-03-39`).

## 7. Conferência de integração

- [ ] 7.1 Abrir a abertura no navegador em dois modos de cor e em largura de celular e de
      aparelho largo, e conferir o que só se vê renderizado: a ordem das dez seções, o par do
      herói legível nos dois modos, e o **efeito colateral registrado** — o herói sem cor da
      família Marca, com o laranja só no símbolo do cabeçalho (design — riscos).
- [ ] 7.2 Conferir que a saída do build serve as dez seções da abertura em HTML real onde o
      PRD-03 §10 exige, que `/quero-participar` continua no `sitemap.xml` e que nenhuma rota do
      núcleo mudou (`RF-03-42`, `RN-03-33`).

## 8. Documentação da change

- [ ] 8.1 Marcar a linha desta change como `implementado` em
      `openspec/cronograma-de-fatias.md`, no bloco do PRD-03, e corrigir o recorte da linha se
      a implementação divergiu do previsto. Verificar que nada mais precisa mudar: o documento
      99 **não** cita a seção de poderes, "Como apoiar" nem o rótulo da chamada, então a relação
      entre documentos não muda; `docs/prds/index.md` segue com o PRD-03 em `implementado`; e
      nenhum arquivo novo nasceu em `docs/`, então a `nav` do `mkdocs.yml` não muda.

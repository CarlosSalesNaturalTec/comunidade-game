# Tasks

## 1. Núcleo

- [ ] 1.1 Criar em `backend/src/nucleo/conteudo_institucional/` o modelo da seção (chave `secao`,
      `texto`, `video_url`, `publicado_em`, `autor_id` nulo para a semeadura), a migração Alembic
      com descida, o registro em `modelos.py` e a operação `conteudo_institucional` em
      `permissoes.py`, sem entrada na matriz de nenhum papel (`RF-02-80`, `RF-03-45`)
- [ ] 1.2 Escrever a regra em `regra.py`: leitura das três seções em ordem fixa, com a ausente
      devolvida sem texto, e a publicação que substitui a versão vigente, grava autor e data,
      exige o texto e aceita `video_url` só em "Quem somos", `https` e opcional (`RF-02-80`,
      `RF-03-45`, `RF-03-49`)
- [ ] 1.3 Expor as rotas em `rotas.py` e registrá-las em `principal.py`: `GET
      /v1/vitrine/conteudo-institucional` pública, sob chave e sem persona, sem o autor na
      saída; `PUT /v1/conteudo-institucional/{secao}` só de Admin, devolvendo autor e data
      (`RF-02-80`, `RF-03-45`, `RF-03-49`, `RF-01-02`)
- [ ] 1.4 Escrever `semeadura.py` e chamá-la em `cli.semear`: "Como apoiar" com a chave PIX e o
      titular do documento 04 §1, "Quem somos" com o rascunho da nota e o bloco "Licenças" do
      `design.md`, "Contatos" vazio, tudo só onde a seção ainda não tem texto (`RF-03-46`,
      `RF-03-48`)

## 2. App 06

- [ ] 2.1 Criar em `apps/app-06-vitrine/src/api/` a leitura do conteúdo institucional e o hook
      `useConteudoInstitucional`, uma leitura por carga de página guardada só em memória, sem
      `localStorage`, `sessionStorage` nem cookie (`RF-03-45`, `RN-03-22`)
- [ ] 2.2 Criar `institucional/` com o componente do texto (parágrafos e `## Título` com `id`
      derivado do título, como texto do React e nunca como HTML) e as três seções: "Quem somos"
      com nota, bloco "Licenças", link do vídeo sem player embutido e rolagem até
      `#nota-de-transparencia-sobre-ia`; "Contatos"; "Como apoiar" com a chave PIX e a frase das
      necessidades em entrega própria. Seção sem texto diz que não foi publicada. Ligá-las em
      `navegacao/recortes.ts`: "Quem somos" abre "sociedade civil", "Como apoiar" e "Contatos"
      fecham, e "Contatos" fecha também os outros dois recortes (`RF-03-45`, `RF-03-46`,
      `RF-03-48`, `RF-03-49`, `RF-03-50`)
- [ ] 2.3 Criar `coleta/` com o aviso discreto de coleta, montado em `App.tsx` para valer em toda
      tela, e a área detalhada em `/o-que-coletamos` (constante em `navegacao/caminhos.ts`, rota
      em `App.tsx`): cada dado com de quem, para quê e por quanto tempo, derivado do PRD-03 §11 e
      do documento 03 §12.2 sem número que eles não tragam, e a declaração de que a vitrine não
      coleta do visitante nem guarda a conversa do assistente (`RF-03-52`, `RF-03-53`,
      `RN-03-23`, `RN-03-22`)

## 3. Testes

- [ ] 3.1 Em `backend/tests/test_conteudo_institucional.py`: três seções em ordem fixa mesmo sem
      publicação, publicação que substitui a vigente com autor e data, texto ausente recusado,
      `video_url` aceito só em "Quem somos" e só em `https`, e publicar sem o link o retira
      (`RF-02-80`, `RF-03-45`, `RF-03-49`)
- [ ] 3.2 Em `backend/tests/test_conteudo_institucional_rota.py`: `GET` sem token e com chave, 401
      sem chave, saída sem o autor, ausência de rota de escrita sob `/v1/vitrine`, `PUT` de Admin
      aceito, recusa 403 de Mestre, Apoiador, responsável e Guerreiro(a), seção inexistente
      recusada e escrita auditada (`RF-02-80`, `RF-03-45`, `RF-01-02`)
- [ ] 3.3 Em `backend/tests/test_conteudo_institucional_semeadura.py`: banco vazio recebe PIX,
      titular, nota e "Licenças" e deixa "Contatos" sem texto, a nota declara construção com
      Claude, atendimento por terceiros, ausência de perfilamento e remissão a "Licenças",
      repetir não altera e a edição de um Admin sobrevive (`RF-03-46`, `RF-03-48`)
- [ ] 3.4 Em `apps/app-06-vitrine/src/testes/conteudoInstitucional.test.tsx`: "Quem somos" com
      nota e "Licenças" sob os seus títulos, âncora da nota abrindo em foco, vídeo como link e
      nenhuma requisição a terceiro, seção sem texto dizendo que não foi publicada, chave PIX em
      "Como apoiar" vinda do núcleo, e a ordem nos três recortes (`RF-03-45`, `RF-03-46`,
      `RF-03-48`, `RF-03-49`)
- [ ] 3.5 Em `apps/app-06-vitrine/src/testes/avisoDeColeta.test.tsx`: aviso em recorte, página de
      Guerreiro(a), página de comunidade e formulários, sem bloqueio e sem confirmação; área
      detalhada com dado, de quem, para quê e prazo, e a declaração de que a vitrine não coleta
      do visitante; `localStorage`, `sessionStorage` e cookie vazios depois de abrir e recarregar.
      Ajustar `semRastro.test.tsx` e `abertura.test.tsx` onde assumiam "Como apoiar" pendente
      (`RF-03-52`, `RF-03-53`, `RN-03-23`, `RN-03-22`)

## 4. Documentação

- [ ] 4.1 Marcar a fatia 5 do PRD-03 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change, e corrigir a fatia 16 do PRD-02 para "só a tela de edição, sobre o
      `PUT` que a fatia 5 entregou". No documento 09 §1: mover a linha da etiqueta de IA para
      dizer que a nota existe em `/#nota-de-transparencia-sobre-ia` e que a etiqueta no texto
      reescrito é de quem entregar a personalização; ajustar a linha da nota, que cita só o
      Gemini no atendimento, aos documentos 01 §7 e 03 §1.12. No PRD-03 §14: o rascunho da nota
      existe e o texto final segue com o fundador. `docs/prds/index.md`, o documento 99 e a `nav`
      do `mkdocs.yml` não mudam — nenhum arquivo nasce em `docs/` e nenhuma relação entre
      documentos muda

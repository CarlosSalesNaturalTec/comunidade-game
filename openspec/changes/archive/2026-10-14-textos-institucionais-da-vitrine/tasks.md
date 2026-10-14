# Tasks

## 1. Documentos-fonte das decisões novas

- [x] 1.1 No `docs/03-plataforma-e-arquitetura.md` §1, princípio 4, gravar a decisão 6 do
  fundador: o auxílio de ferramentas de IA não altera a licença do artefato — código em AGPL,
  conteúdo e dados em CC BY-SA, crédito de quem decidiu, revisou e publicou. Uma a duas frases,
  dentro do princípio que já rege licença e marca; verificar que nenhuma regra foi duplicada e
  que a reserva da marca, já escrita ali, não mudou de sentido. (`RF-03-48`)
- [x] 1.2 Gravar o canal de contato onde cada assunto tem a sua fonte: no
  `docs/03-plataforma-e-arquitetura.md` §8, na descrição de "Contatos", o **endereço único** do
  projeto, o que ele atende e que ele nunca alcança um Guerreiro(a); e no
  `docs/04-modelo-economico-e-sustentabilidade.md` §1, em "Doações em espécie — canal oficial",
  a remissão em uma frase ao canal, no lugar de "a pessoa jurídica vinculada" sem endereço.
  Verificar que o endereço aparece em **um** documento só e que a regra de não guardar dado
  fiscal continua idêntica. (`RF-03-45`, `RF-03-46`)

## 2. Pauta do fundador e PRD

- [x] 2.1 No `docs/09-topicos-em-aberto-e-sugestoes.md`, acrescentar a "Já decididos" as cinco
  linhas das decisões de 2026-10-14: canal único de contato para todas as finalidades; nota de
  transparência sobre IA como texto final; licença do gerado com auxílio de IA; "Quem somos" só
  no recorte padrão; marca reservada declarada na vitrine. Cada linha cita o documento-fonte, e
  nenhuma repete a regra inteira. Verificar que nada foi acrescentado a "Decisões pendentes".
- [x] 2.2 No `docs/prds/prd-03-vitrine-publica.md` §14, remover a pendência do texto final da
  nota de transparência, registrando que a decisão do fundador de 2026-10-14 a fechou e que o
  `RF-03-48` deixa de estar travado no texto. A pendência do título da criação original
  permanece. Verificar que a §15 (rastreabilidade) continua correta sem alteração, já que
  nenhum `RF` mudou de origem. (`RF-03-48`)

## 3. Semeadura das três seções

- [x] 3.1 Em `backend/src/nucleo/conteudo_institucional/semeadura.py`, reescrever
  `TEXTO_DE_QUEM_SOMOS` com os blocos do `design.md` § Textos: a apresentação institucional
  antes de "## Nota de transparência sobre IA", a nota **byte a byte como está hoje**, e o
  bloco "## Licenças" substituído pela versão com os dois parágrafos novos. Verificar, lendo a
  constante, que o título da nota não mudou nenhum caractere. (`RF-03-45`, `RF-03-48`)
- [x] 3.2 Na mesma semeadura, acrescentar `TEXTO_DE_CONTATOS` com o texto do `design.md`, e
  registrá-lo em `SEMENTES`, de modo que as três seções passem a nascer com texto. Atualizar o
  comentário da função, que hoje afirma que "Contatos" fica vazio por não haver contato em
  documento nenhum, e o comentário do módulo, citando a decisão do fundador de 2026-10-14.
  Verificar que a convergência segue gravando só onde a seção não tem texto. (`RF-03-45`)
- [x] 3.3 Na mesma semeadura, acrescentar a `TEXTO_DE_COMO_APOIAR` o comprovante obrigatório e a
  regra do recibo com o endereço, conforme o documento 04 §1 e o `design.md`. Verificar que a
  chave PIX e o titular continuam idênticos aos do documento 04 §1, caractere por caractere.
  (`RF-03-46`)

## 4. Testes da semeadura

- [x] 4.1 Em `backend/tests/test_conteudo_institucional_semeadura.py`, substituir o teste que
  hoje afirma `contatos.texto is None` por um que cubra os cenários "Banco novo recebe as três
  seções com texto" e "Nenhuma seção nasce com vídeo" do delta: as três seções com texto, a
  chave PIX e o titular em "Como apoiar", a apresentação e os dois blocos em "Quem somos", o
  endereço em "Contatos", `video_url` nulo nas três e `autor_id` nulo. Renomear o teste, cujo
  nome atual declara que "contatos fica vazio". (`RF-03-45`, `RF-03-46`, `RF-03-49`)
- [x] 4.2 No mesmo arquivo, estender a cobertura da nota e de "Licenças" para os cenários "O
  título da nota é o que a etiqueta de IA ancora", "'Licenças' declara o auxílio de IA e a marca
  reservada" e "'Contatos' traz um endereço único, que não alcança criança": o título exato do
  bloco da nota, a frase do auxílio de IA, a reserva da marca e a declaração de que nenhum canal
  alcança um Guerreiro(a). Manter intacto o teste de que repetir a semeadura não desfaz a edição
  do Admin. (`RF-03-48`, `RF-03-45`)
- [x] 4.3 Verificar que `apps/app-06-vitrine/src/testes/conteudoInstitucional.test.tsx`, que
  fixa o identificador `nota-de-transparencia-sobre-ia`, continua passando sem alteração — se
  exigir mudança, o título da nota foi alterado e a tarefa 3.1 está errada. (`RF-03-48`)

## 5. Fechamento

- [x] 5.1 Acrescentar ao `openspec/cronograma-de-fatias.md`, no bloco do PRD-03, a linha desta
  change com `—` na coluna de fatia, no padrão da `2026-10-11-vitrine-reordenada-e-entrada-verde`:
  as nove decisões, o fechamento da pendência da nota no PRD-03 §14 e a situação. Conferir que a
  situação do PRD-03 em `docs/prds/index.md` **não** mudou — a change não altera a fase do PRD —
  e, nesse caso, não tocar no arquivo; conferir igualmente que nenhuma relação entre documentos
  mudou, já que o licenciamento continua tendo o documento 03 §1 como fonte única, e portanto o
  `nav` do `mkdocs.yml` fica como está. O documento 99 §3 **recebe** a linha do canal de
  contato, porque o documento 04 §1 passou a remeter ao 03 §8 — relação nova entre documentos.
- [x] 5.2 Registrar no `design.md`, em uma linha ao fim de Decisions, os dois passos que ficam
  com o fundador por serem operação e não código: publicar as três seções por
  `PUT /v1/conteudo-institucional/{secao}` na App 03, porque a semeadura não alcança a produção
  já semeada, e fazer o redeploy da App 06, sem o qual "Quem somos" e "Contatos" não aparecem no
  site. Verificar que nenhuma tarefa desta change tenta executá-los.

## Workflow follow-up

- Arquivar a change depois da aprovação do fundador, consolidando o delta de
  `conteudo-institucional` em `openspec/specs/`.

PRD-04 (App 01 — Aula presencial), **fatia 14** — fatia nova, não prevista, acrescentada ao
`openspec/cronograma-de-fatias.md` com esta change. Atende `RF-04-63`, `RN-04-32`, `RN-04-33` e
a ampliação do `RF-04-26`.

**Depende do PR de revisão do PRD-04** (branch `claude/prd-04-bancada-de-calibracao-vhowej`),
que cria os três identificadores acima. Esta change não merge antes dele.

## Why

O limiar de comparação do descritor em produção vale **0,5** — a convenção do `face-api.js`,
de descritor normalizado de 128 posições. A biblioteca Human não normaliza o descritor dela, e
a fronteira de _match_ que a própria biblioteca documenta equivale a **~10** na distância
euclidiana que o núcleo calcula. Com 0,5, nenhuma criança seria reconhecida.

O modo de falhar é o que torna isto urgente: a comparação que não confere **não gera erro**.
Ela registra "recusa" na auditoria, a criança entra pela confirmação humana, e ninguém descobre
que o reconhecimento nunca funcionou — é o mesmo desfecho de quem não tem _template_.

O valor certo não se deduz: depende da câmera do aparelho e da luz da sala. Precisa ser medido
**onde a aula acontece**, e é para isso que a bancada existe.

## What Changes

- A App 01 ganha a **tela de medição** do `RF-04-63`, alcançável por Mestre ou Admin em sessão
  de trabalho: captura, compara descritores **no aparelho** e mostra a distância na unidade que
  o núcleo usa. Nada é enviado ao núcleo.
- A tela guarda **um** descritor de referência por vez e descarta cada captura comparada no
  mesmo ato (`RN-04-32`); sobre Guerreiro(a) ela só é oferecida **dentro do onboarding, depois
  do consentimento registrado** (`RN-04-33`).
- O **aviso de coleta** e a área detalhada de direitos passam a declarar a medição
  (`RF-04-26`).

Fica **fora**: trocar o secret `cg-biometria-limiar-de-comparacao` pelo valor medido — é ato de
implantação, e só existe depois de a bancada rodar num encontro real. Entra como tarefa em
aberto, no molde da change do CORS do bucket. Também fica fora a correção da dimensão do
descritor, que é da change `dimensao-do-descritor-e-recusa-legivel-na-captura` — sem ela a
bancada mede, mas nenhuma captura grava.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: requisito novo para a tela de medição — quem a alcança, o que
  ela guarda e descarta, e a restrição de só operar sobre Guerreiro(a) dentro do onboarding. E o
  Requirement "A área detalhada diz o destino de cada dado e o canal do responsável" passa a
  incluir a medição entre os dados que a área declara.

O `template-biometrico` **não muda**: a medição não toca o núcleo, não grava _template_ e não
gera acesso auditável — ela compara dois descritores que nasceram e morreram no aparelho.

## Impact

- `apps/app-01-aula-presencial/`: a tela de medição, o caminho que a alcança no
  `FluxoDeOnboarding` e na tela inicial, e a área detalhada de direitos.
- `comum/biometria/`: a função que calcula a distância euclidiana, espelhando a do núcleo — é a
  primeira vez que o cálculo existe no aparelho, e precisa dar o **mesmo número** que
  `_distancia_euclidiana` dá no backend, ou a medição não serve para escolher o limiar.
- **Sem backend**: nenhuma rota, nenhum contrato de API, nenhuma migração.
- **Ato de implantação**, fora do alcance da sessão de implementação: gravar no secret
  `cg-biometria-limiar-de-comparacao` o valor medido, no lugar de 0,5.

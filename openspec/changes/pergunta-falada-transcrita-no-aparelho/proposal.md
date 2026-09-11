# Pergunta falada transcrita no aparelho

Origem: **PRD-04** (fatia sem número, `Pergunta falada transcrita no aparelho` — `RF-04-39`,
`RF-04-40`, `RN-04-21`). Aplica ao código a decisão do fundador de 2026-09-10, já registrada no
documento 03 §§1.12, 7, no documento 09 §1 e no enunciado novo de `RF-04-40` e `RN-04-21`: a
fala vira texto no próprio aparelho, e ao núcleo chega texto.

## Why

As fatias 10 a 12 entregaram o assistente de trilhas com a pergunta falada indo ao núcleo como
áudio, transcrita lá pelo Gemini. Três coisas mudaram desde então:

1. **A proteção da criança fica mais forte.** O áudio deixa de trafegar e deixa de existir do
   lado do núcleo — não é recebido, não passa por memória de servidor, não entra em log. O
   `RF-04-40` que antes prometia descartar depois de transcrever passa a prometer que o áudio
   **não chega**.
2. **A pergunta falada volta a funcionar.** O Gemini perdeu o _free tier_ para conta nova, e as
   três portas de IA respondem indisponibilidade por falta de crédito (change
   `2026-09-10-chave-do-gemini-em-producao`). Transcrever no navegador destrava a fala sem
   depender de crédito de provedor — o mesmo desenho que já resolve a biometria facial do App 01
   no próprio aparelho.
3. **O custo desaparece.** Áudio é a entrada mais cara das três portas de IA, e a passada
   multimodal que transcrevia e respondia junto vira uma passada de texto.

## What Changes

- **BREAKING** na rota `POST /v1/assistente/trilhas/consultas`: `texto` passa a ser
  **obrigatório** e o campo `arquivo` **deixa de existir**. Não há consumidor externo — a única
  chamadora é a App 01, que muda no mesmo PR.
- `PortaDoAssistente.responder` perde o parâmetro `arquivo`: o adaptador de produção manda só
  texto ao Gemini, e o adaptador local para de simular transcrição de áudio.
- A App 01 transcreve a fala pela **Web Speech API** do navegador e envia a transcrição como
  texto. O microfone segue abrindo por toque e fechando ao fim da fala (`RF-04-39`), e nenhum
  áudio é gravado nem mantido no aparelho.
- A transcrição aparece no campo de pergunta **antes do envio**, editável — o documento 09 §1
  registra que o fundador aceitou isso, e que por causa disso a forma "áudio" passa a valer o
  mesmo que a forma "texto".
- Onde o navegador não oferece a API (Firefox, desligada por padrão), a tela **avisa e mantém o
  registro por texto digitado**, que já era o caminho de sempre — não é funcionalidade nova, é
  requisito de tela.
- A transcrição no aparelho entra em `comum/`, como a biometria: as duas telas que precisam dela
  são da App 01 e da App 05, e a fatia irmã do PRD-05 a consome sem duplicar código.

## Capabilities

### New Capabilities

Nenhuma. Nem a consulta ao assistente nem a tela dele são novas: a fatia troca **como** a
pergunta falada chega.

### Modified Capabilities

- `consulta-ao-assistente`: a pergunta chega **sempre em texto**. Cai a exigência de exatamente
  uma forma entre texto e áudio, cai a transcrição no núcleo e cai o descarte do áudio depois
  de transcrito — o que sobra é mais forte: o áudio nunca chega (`RF-04-40`, `RN-04-21`).
- `aplicacao-da-aula-presencial`: o microfone segue abrindo por toque e fechando ao fim da fala,
  mas o que a tela envia é **a transcrição**, não o áudio; e a tela declara o que faz onde o
  navegador não transcreve (`RF-04-39`, `RF-04-40`, `RN-04-20`, `RN-04-21`).

A linha da fatia no `openspec/cronograma-de-fatias.md` diz que o contrato "quase não muda" e a
linha da fatia irmã do PRD-05 diz que esta não tem delta de spec. **Tem**: a consulta não grava
a forma da pergunta, mas as duas specs acima descrevem o áudio chegando ao núcleo, e isso deixa
de ser verdade. O recorte (`RF`/`RN`) não muda; as duas linhas do cronograma são corrigidas
nesta change, como o `openspec/config.yaml` manda fazer quando o cronograma divergir.

A entrega da produção por fala **não entra aqui** — é a fatia irmã do PRD-05, que depende desta
e alcança as telas das Apps 01 e 05. `producoes` segue recebendo áudio e foto até lá.

## Impact

| Área                                                           | O que muda                                            |
| -------------------------------------------------------------- | ----------------------------------------------------- |
| `comum/fala/`                                                  | módulo novo: transcrição pela Web Speech API          |
| `comum/package.json`                                           | subcaminho `./fala` exportado                         |
| `backend/src/nucleo/assistente/rotas.py`                       | `texto` obrigatório, `arquivo` removido               |
| `backend/src/nucleo/assistente/{porta,regra,local,nuvem}.py`   | a porta deixa de receber áudio                        |
| `apps/app-01-aula-presencial/src/trilhas/TelaDoAssistente.tsx` | fala transcrita no aparelho, transcrição editável     |
| `apps/app-01-aula-presencial/src/api/assistente.ts`            | a chamada manda só texto                              |
| `openspec/cronograma-de-fatias.md`                             | a situação da fatia e a correção das duas linhas      |
| `docs/prds/index.md`                                           | nada: a situação do PRD-04 não muda                   |

Sem migração de banco: `ConsultaAoAssistente` já guardava só as transcrições, e nenhuma coluna
registra a forma da pergunta.

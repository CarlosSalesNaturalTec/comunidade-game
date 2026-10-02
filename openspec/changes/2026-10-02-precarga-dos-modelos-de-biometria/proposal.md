# Proposal

Origem: **fatia 24 do PRD-04** (`openspec/cronograma-de-fatias.md`). Fecha a primeira pendência
da **§14 do PRD-04** — "peso dos modelos da biblioteca Human no primeiro carregamento, contra o
requisito de aparelho modesto e rede instável".

Recorte: `RF-04-75` e `RN-04-42` (**novos**, a criar na revisão do PRD-04), alcançando
`RF-04-13`, `RF-04-48`, `RF-04-65` e `RN-04-12`.

## Why

**Os modelos caem no pior momento possível.** `comum/biometria` só busca os modelos dentro de
`prepararCaptura()`, que roda quando uma tela de câmera abre — o onboarding, a entrada por
reconhecimento, a bancada de medição. Na prática: a **primeira criança diante da câmera**, com a
turma entrando pela porta. O peso foi medido no pacote fixado (`@vladmandic/human@3.3.6`):

| Modelo | Tamanho |
| --- | --- |
| `faceres` | 6.885 KB |
| `facemesh` | 1.537 KB |
| `antispoof` | 842 KB |
| `blazeface` | 604 KB |
| `liveness` | 596 KB |
| **Total** | **10,22 MB** |

Isso colide com o documento 03 §3.4, que exige "registro de presença de Guerreiro(a) conhecido
em **poucos segundos** — a aula não pode travar na porta", e com o aparelho modesto do §3.2.

**O que o fundador pediu, e o que a elicitação mostrou.** O pedido original era tela com barra de
progresso após o login, e o menu principal só ao concluir. Isso é um **portão bloqueante**, e
contraria duas coisas: o documento 03 §3.4 acima, e o `RF-04-23` — sem rede a presença entra em
fila local, e com o portão o aparelho que chega sem rede não alcançaria nem a fila. O Mestre
ficaria na porta, com a turma entrando e uma barra parada. Decidida, em 2026-10-02, a **pré-carga
ao fundo, que nunca bloqueia**.

**Duas medições recortaram a fatia, e as duas desmentem o desenho óbvio:**

1. **O cache durável já existe.** `cacheModels` tem `default: true` em navegador na versão
   fixada, e `comum/biometria/biometria.ts` não o desliga. Os 10,22 MB caem **uma vez por
   aparelho** e sobrevivem entre sessões. O problema nunca foi a repetição — é só *quando* a
   única vez acontece.
2. **A Human expõe progresso por modelo, não por byte.** `human.models.loaded()` devolve a lista
   carregada, e `human.events` dispara `load`. Isso dá **5 passos**, não percentual contínuo.

**Por isso service worker e app instalável ficam de fora.** A durabilidade que os justificaria já
está resolvida pelo IndexedDB; um service worker cacheando os mesmos 10,22 MB criaria uma segunda
fonte de verdade para um cache que funciona. O ganho restante — shell offline e instalabilidade —
é outro problema, é decisão **das oito** e mora no documento 03, não numa fatia da App 01; e o
invariante 1 do documento 99 §6 ("todas Web Apps responsivos, Mobile First. Sem app nativo") a
condiciona. Some-se o modo de falha: num aparelho de sala raramente recarregado, "a aplicação
mostra a versão do mês passado e não atualiza" é pior, para um Mestre que não depura nada, que
uma primeira captura lenta.

## What Changes

- **`comum/biometria` ganha a pré-carga**, que carrega os modelos **sem tocar a câmera**.
  `prepararCaptura()` segue como está e encontra tudo pronto — `load()` é idempotente.
- **A App 01 dispara a pré-carga ao abrir a sessão de trabalho do aparelho**, ao fundo, só com
  rede, e **nunca espera por ela** para apresentar a tela inicial ou qualquer caminho.
- **Um indicador discreto** mostra o andamento, em 5 passos. Ele **não é portão**: nenhuma tela
  depende dele, e ele some ao concluir.
- **Falha da pré-carga é silenciosa.** O caminho de erro na tela continua sendo o de
  `prepararCaptura()` (`RF-04-65`), que não muda.
- **PRD-04**: a §14 perde a pendência do peso dos modelos; nascem `RF-04-75` e `RN-04-42`.
- **Documento 03 §3.4** registra a pré-carga como resposta ao requisito de poucos segundos;
  **documento 09 §1** recebe a decisão nova e a descartada (service worker / PWA).

## Impact

- `comum/biometria/biometria.ts` e `indice.ts`: uma função exportada a mais.
- `apps/app-01-aula-presencial/src/sessao-de-trabalho/`: o disparo e o indicador.
- `apps/app-01-aula-presencial/src/testes/configuracao.ts`: o dublê da função nova — sem ele o
  jsdom tentaria carregar 10,22 MB em toda suíte.
- `docs/prds/prd-04-aula-presencial.md` §§6, 14; `docs/03-plataforma-e-arquitetura.md` §3.4;
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1.
- **Fora do escopo:** a App 05, que também consome `comum/biometria`. A função nasce em `comum/`
  e fica disponível a ela, mas o disparo é só da App 01 — a App 05 não tem sessão de trabalho de
  aparelho, e o momento equivalente é decisão do PRD-05.

## Decisões recebidas na elicitação

Duas questões foram levadas ao fundador em **2026-10-02** e respondidas antes de os artefatos
fecharem:

- **O indicador entra**, e com ele o `RF-04-75`. A alternativa — pré-carga silenciosa, sem `RF`
  novo, que a §14 do PRD-04 já cobriria como desenho de implementação — foi descartada.
- **O disparo é ao abrir a sessão de trabalho do aparelho**, e não só com a aula já escolhida.
  Poupar o aparelho que abriu por engano não compensa chegar atrasado na primeira captura.

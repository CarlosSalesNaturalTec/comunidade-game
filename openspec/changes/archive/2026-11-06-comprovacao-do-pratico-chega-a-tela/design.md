# Design

## Context

Aplica o que já está consolidado em `openspec/specs/desbloqueio-da-missao`,
`area-do-guerreiro`, `aplicacao-da-aula-presencial` e `area-do-mestre` desde a fatia 13 do
PRD-05. O núcleo está certo e não muda: `DesafioDeDesbloqueioSaida`
(`backend/src/nucleo/trilhas/rotas.py`) serve `forma_de_comprovacao`, `criterio_de_aceite` e
`titulo_curto`, e `_conferir_envio_da_comprovacao` (`regra.py`) já aceita abrir a sessão de
envio numa declaração em mídia **pendente e sem arquivo**. O defeito é só de leitura na tela.

```text
núcleo (percurso)                    tela (comum/trilha)
desafio_de_desbloqueio.              desafio.
  forma_de_comprovacao   ──── ✗ ───►  desafio_pratico_forma_de_comprovacao  → undefined → null
  criterio_de_aceite     ──── ✗ ───►  desafio_pratico_criterio_de_aceite    → undefined → null
                                      ⇒ "prático antigo": só "Já cumpri!"
```

## Decisions

1. **Corrige-se a tela, não o núcleo.** Os nomes curtos são os da resposta testada do
   percurso e da declaração; os longos (`desafio_pratico_*`) seguem só na leitura do Mestre
   (`MissaoSaida`), onde a App 09 já os lê certo. Descartada: renomear o núcleo — mexe em
   resposta já testada e na leitura do Mestre, para nada.
2. **Exemplo de contrato único em `comum/contratos/missao-no-percurso.json`**: uma resposta do
   percurso com prático em imagem. O teste do núcleo monta o mesmo cenário e afirma que o
   conjunto de chaves de `desafio_de_desbloqueio` e de `comprovacao_entregue` é **igual** ao do
   exemplo; os testes das telas importam o exemplo em vez de escrever o objeto à mão.
   `backend-ci.yml` passa a disparar também por `comum/contratos/**`. Descartadas: gerar tipos
   do OpenAPI (ferramenta nova, decisão de stack fora desta correção) e afirmar os nomes só de
   um lado (foi o que deixou o defeito passar).
3. **O `?? null` fica, mas só para o que o núcleo serve nulo.** Com a interface certa, campo
   ausente deixa de ser possível em TypeScript; o comentário que justificava o "ausente" sai.
4. **Retomada da declaração sem arquivo.** No ramo "aguardando o Mestre", quando
   `forma` é mídia, `entrega_presencial` é falso e `tem_arquivo` é falso, a tela mostra o aviso
   da mídia guardada, diz que o arquivo não chegou e oferece o seletor e "Enviar o arquivo",
   pela mesma `enviarArquivoDaComprovacao` (progresso e retomada inclusos). Concluído, a tela
   recarrega a missão e mostra "O seu arquivo foi enviado e está guardado." Nenhuma rota nova.
   Descartada: pedir ao Mestre que recuse para reabrir — funciona, mas registra "não cumpriu"
   para quem não errou.
5. **"O que você entregou" só com conteúdo.** O título aparece quando há texto ou arquivo; a
   entrega no encontro mantém a frase própria.
6. **Bancada da App 09**: a frase "O envio do arquivo ainda não concluiu." sai. Sem texto nem
   arquivo, a tela usa `comprovacao_entregue.forma`: nula → "Este desafio não pedia
   comprovação quando foi declarado."; mídia → "O arquivo não chegou. O Guerreiro(a) ainda pode
   enviá-lo pela tela da missão até você julgar." Os controles de julgamento seguem.

## Risks / Trade-offs

- `forma` em `comprovacao_entregue` é a **atual** da missão, não a da hora da declaração: uma
  declaração feita sem forma e redeclarada depois em mídia (o caso do Bruno) passa a ser
  tratada como mídia sem arquivo — e é o que se quer, porque agora ela pode recebê-lo.
- Declarações do período do defeito ficam como estão no banco; a decisão 4 as recupera pela
  tela, sem migração.

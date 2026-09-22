## Context

Ver `proposal.md` — Why. O núcleo já chega pronto: a fatia anterior torna a aula opcional,
resolve o limiar pela comunidade e dá ao responsável a operação com escopo. Esta fatia é
inteiramente de tela, em `apps/app-05-guerreiro/`.

O padrão do tratamento de erro já foi decidido e implementado na App 01, na change
`2026-09-21-aula-na-entrada-e-erro-de-camada-legivel`: a recusa se reconhece pelo código
`autenticacao_biometrica_invalida` do corpo único, e o que roda depois da conferência tem
tratamento próprio. Aqui ele é aplicado, não redecidido.

## Goals / Non-Goals

- **Goal**: a App 05 passa a ter entrada em casa — por reconhecimento e, quando ele recusa, pelo
  responsável.
- **Non-Goal**: o núcleo. Fatia anterior.
- **Non-Goal**: o espelho e o visor ao vivo da App 05, que são recorte do PRD-05 e seguem como
  estão; esta fatia não mexe na captura.
- **Non-Goal**: rever o que a App 05 deixa a criança fazer depois de entrar.

## Decisions

**1. A ausência da aula é declarada, não esquecida.** A entrada da App 05 chama a conferência
sem aula porque ali não há encontro — e o código diz isso, com comentário que amarra ao
`RN-01-57`. Sem essa declaração, um leitor futuro leria a ausência como o mesmo defeito que
quebrou a App 01 e "consertaria" enviando uma aula qualquer.

**2. A sessão assistida troca de dono, não de forma.** `ConfirmacaoAssistida` já monta um
`ProvedorDeSessao` próprio, com chave de armazenamento distinta, que se encerra assim que a
sessão da criança abre. A estrutura serve igual ao responsável; muda quem se autentica e como.
_Alternativa descartada_: uma tela nova só para o responsável — duplicaria o cuidado de não
deixar a sessão do adulto sobreviver ao ato.

**3. Os dois caminhos de login convivem na mesma tela.** `entrarComGoogle` e
`entrarComCredencial` já existem no `ContextoDeSessao`. A tela oferece os dois, sem perguntar
antes qual o adulto tem.
_Alternativa descartada_: escolher o caminho por uma pergunta prévia — uma tela a mais entre a
criança recusada e a sessão aberta, sem ganho.

**4. A troca de senha provisória acontece dentro da sessão assistida.** O `ContextoDeSessao` já
distingue `trocaDeSenhaPendente` de sessão inválida e já expõe `trocarSenhaProvisoria`; o que
falta é a tela. Ela entra **dentro** do fluxo da confirmação, e ao concluir segue direto para
abrir a sessão da criança.
_Alternativa descartada_: mandar o responsável trocar a senha na App 07 e voltar — é sair da
aplicação no meio de um resgate, com a criança esperando.

**5. A recusa por criança alheia usa a frase da recusa comum.** O núcleo já devolve resposta
indistinguível; a tela não pode desfazer isso escrevendo "essa criança não é sua".

## Risks / Trade-offs

- **A tela da sessão assistida acumula quatro estados** — escolher login, autenticar, trocar
  senha provisória, confirmar — → os cenários do delta cobrem cada um, e a alternativa é
  espalhar o fluxo por telas que a criança recusada teria de atravessar esperando.
- **Um adulto com sessão aberta no aparelho de casa** → o provedor próprio com chave distinta já
  existe e encerra a sessão do adulto assim que a da criança abre; o cenário que afirma isso
  continua valendo.
- **A App 05 depende de uma fatia que ainda não entrou** → é dependência de ordem, declarada no
  cronograma e no plano de migração.

## Migration Plan

Sem migração: mudança de cliente, sem dado gravado. A entrada volta a funcionar no _deploy_ da
App 05, contra o núcleo que a fatia anterior entrega.

**Ordem obrigatória**: `2026-09-22-limiar-da-comunidade-e-sessao-pelo-responsavel` entra antes.
Sem ela, o pedido sem aula é recusado por campo em falta e o responsável recebe 403.

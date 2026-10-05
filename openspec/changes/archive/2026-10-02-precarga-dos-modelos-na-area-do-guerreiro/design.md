# Design

## Context

`precarregarModelos()` e `andamentoDosModelos()` já estão em `comum/biometria`, entregues pela
fatia 24 do PRD-04, e a App 05 já consome o módulo em `TelaDeEntradaDoGuerreiro.tsx`. A fatia é
inteiramente de aparelho: nenhuma rota, nenhuma migração, nenhum lançamento no livro-razão.

A tela de entrada já tem o efeito que decide entre `verificandoCamera`, `entrada` e
`confirmando`, e é nele que a verificação da câmera acontece — o ponto que o fundador escolheu.

## Goals / Non-Goals

**Goals:**

- Tirar o download dos modelos de cima da criança já na frente da câmera.
- Dizer a ela o que está acontecendo, sem transformar isso em erro.

**Non-Goals:**

- Mexer no caminho de erro da conferência: `RN-05-48` e o invariante 25 continuam valendo, e a
  falha da pré-carga NEVER veste a frase do rosto.
- Componente de progresso em `comum/react`: a fatia 24 do PRD-04 já registrou que `Aviso` atende
  e que componente comum sem segundo consumidor é peso sem uso — aqui o segundo consumidor
  aparece, e continua atendido por `Aviso`.
- Pré-carga na App 07, na App 08 ou na App 09: nenhuma delas entra por reconhecimento.

## Decisions

### 1. O disparo é depois de `existeCamera()`, dentro do efeito que já existe

Decisão do fundador, 2026-10-02, entre três momentos possíveis. Os outros dois foram
descartados: na montagem da casca da aplicação, a pré-carga pegaria também quem já tem sessão
restaurada e nunca abre a câmera; na montagem da tela de entrada, pegaria o aparelho sem câmera,
que o `RF-05-02` recusa e que vai ao adulto do `RN-05-02` sem nunca gerar descritor. Depois da
verificação, a pré-carga só acontece onde vai ser usada — e o piso de rede e de aparelho, que o
fundador decidiu em 2026-09-30 **não afrouxar**, é respeitado por construção.

O gatilho da App 01 não serve: `if (!sessao || sessao.papel === "guerreiro") return;` exige
sessão aberta e exclui o papel Guerreiro(a). Na App 05 quem é reconhecido não tem sessão.

### 2. Sai com indicador, e por isso nascem `RF-05-90` e `RN-05-49`

Decisão do fundador, 2026-10-02. A alternativa — pré-carga silenciosa, que não pediria `RF`
novo — foi descartada. O precedente governa a forma: `RF-04-75` e `RN-04-42` nasceram na §6.1 do
PRD-04 pela mesma razão, e `RN-05-49` desce do `RN-05-01` e do documento 03 §3.3, como
`RN-04-42` desceu do `RN-04-07` e do mesmo §3.3.

### 3. O andamento usa `Aviso tipo="andamento"`; a falha não

Mesma conclusão da fatia 24 do PRD-04, e pela mesma leitura de `comum/react/Aviso.tsx`: os dois
tipos vermelhos (`erro`, `atencao`) mapeiam `role="alert"` e **interrompem**, e `andamento`
mentiria no rótulo se dissesse "falhou". A falha sai do `Aviso` e vira linha local de
`role="status"`, no molde do `EstadoDaLista`. O fundador já fixou a prioridade em 2026-10-02:
**não interromper; se for preciso, abrir mão do vermelho.**

### 4. A submissão espera o que faltar, em vez de ser recusada

Se a pessoa digitar o nick e submeter antes de a pré-carga terminar, `gerarDescritor()` encontra
o que já veio e carrega o resto — `precarregarModelos()` é idempotente com `prepararCaptura()`,
e os modelos ficam em IndexedDB entre sessões. Nada de novo precisa ser escrito para isso; o que
a tela NEVER faz é bloquear o campo.

## Risks / Trade-offs

- **O primeiro Guerreiro(a) do dia paga o download; os seguintes, não.** `cacheModels` vale
  `true` por padrão e os modelos ficam em IndexedDB. Num aparelho compartilhado de ponto de
  apoio, o ganho da pré-carga é concentrado na primeira entrada — e é exatamente ali que a
  espera hoje é pior.
- **Um indicador a mais numa tela de criança.** O risco é ruído visual na porta de entrada. É o
  preço da decisão 2, e o `RF-05-90` o limita: informação, nunca alerta, e sem depender de cor.
- **Aparelho que ganha câmera depois** (permissão concedida numa segunda tentativa) só
  pré-carrega quando a verificação roda de novo. Aceito: a entrada já se reapresenta nesse
  caminho, e forçar a pré-carga antes da permissão contrariaria a decisão 1.

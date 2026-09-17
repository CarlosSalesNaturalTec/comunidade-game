## Context

Ver `proposal.md` — Why. O que o desenho precisa saber: `comum/biometria` já é o único módulo
que toca a câmera e produz descritor, e a fronteira que ele estabelece — só `boolean` e
`number[]` saem dele — é o que garante o invariante 12 por construção. A bancada vive **dentro**
dessa fronteira: ela consome as mesmas duas funções que a `TelaDeCaptura` consome.

A comparação do núcleo é `sqrt(Σ(a-b)²)` sobre o descritor cru, em
`backend/src/nucleo/biometria/regra.py`.

## Goals / Non-Goals

**Goals:** produzir, no aparelho do encontro, o número que permite escolher o limiar; e deixar
de pé a ferramenta que responde "por que esta criança não é reconhecida?".

**Non-Goals:** trocar o valor do limiar (ato de implantação, depois da medição); qualquer
mudança no núcleo; e a correção da dimensão do descritor, que é de outra change.

## Decisions

**1. O cálculo nasce em `comum/biometria` e espelha o do núcleo.** A distância precisa ser
**o mesmo número** que o backend calcula, ou a medição não serve para escolher o limiar. É a
primeira duplicação deliberada de lógica entre as duas pontas deste repositório, e ela se
justifica porque o número tem de ser comparável — o teste de unidade fixa valores conhecidos
para que as duas implementações não divirjam em silêncio. _Alternativa descartada:_ uma rota no
núcleo que calcule a distância — mandaria descritor de criança pela rede para uma finalidade
que não é identificar, contra a finalidade única do `RN-04-06`.

**2. A referência é substituível, e a substituição é explícita.** Trocar a referência é um ato
de quem opera, não um efeito colateral de capturar de novo: sem isso, medir "A contra A" e "A
contra B" na mesma sessão vira adivinhação sobre o que está guardado. _Alternativa descartada:_
guardar uma lista de capturas e comparar todas contra todas — mede mais rápido, e contraria
`RN-04-32`.

**3. Dois caminhos até a tela, com alcance diferente.** Pela tela inicial, em sessão de
trabalho, ela mede **apenas quem opera** — é o caminho do diagnóstico. Pelo passo da imagem do
`FluxoDeOnboarding`, depois do termo, ela mede **o Guerreiro(a) daquele cadastro** — é o
caminho da calibração. A distinção não é de interface: é `RN-04-33`, e é o que torna a garantia
do consentimento verificável no código em vez de confiada a quem opera.

**4. A tela não é secreta, é restrita.** "Caminho não divulgado" não é mecanismo de proteção. O
que a protege é a sessão de trabalho de Mestre ou Admin, que a aplicação já exige — o mesmo
alcance que abre o onboarding.

## Risks / Trade-offs

**As duas implementações da distância divergem com o tempo** → o teste com valores fixos as
prende; se o núcleo mudar o cálculo, o teste do aparelho quebra junto e o defeito aparece no CI,
não no encontro.

**A medição com adultos não representa a face de criança** → é por isso que `RN-04-33` permite
medir sobre Guerreiro(a) sob o termo. O caminho do diagnóstico, com adultos, dá a ordem de
grandeza; a calibração real acontece no onboarding do encontro.

**Descritor de criança na memória do aparelho, ainda que por instantes** → é a mesma exposição
que a captura já tem, e `RN-04-32` a mantém no mesmo grau: um de referência, o comparado
descartado no ato. A tela nunca o apresenta.

## Migration Plan

1. Nenhuma migração, nenhuma rota, nenhuma mudança de contrato.
2. _Deploy_ da App 01 com a tela.
3. Medição num encontro real, pelo Mestre, no aparelho do encontro.
4. Gravar o valor medido no secret `cg-biometria-limiar-de-comparacao`, à mão.
5. _Rollback_: reverter o _merge_. O limiar em produção não muda por esta change, então não há
   estado a desfazer.

## Open Questions

Nenhuma. As quatro decisões que este desenho exigia — onde a bancada vive, se permanece, em
quem abre a câmera e o que guarda — foram tomadas pelo fundador em 2026-09-17 e estão no
PRD-04.

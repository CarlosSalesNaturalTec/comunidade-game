# 06 — Trilha Robô Educa (1ª Trilha da plataforma — Poder da IA e Robótica)

> **Autoria:** Mestre fundador. É a **primeira trilha** da plataforma
> ([02 §3](02-conceito-do-jogo-e-gamificacao.md#as-duas-primeiras-trilhas-da-plataforma)).
>
> O Robô Educa é também a base técnica da **App 02 — Assistente por voz e Modo Ouvinte**
> ([03 §4](03-plataforma-e-arquitetura.md#4-app-02--assistente-por-voz-e-modo-ouvinte)).
>
> Os títulos de **Mecânica** e **Programação** do acervo Include são o **material de apoio**
> desta trilha
> ([02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut)).

O **Robô Educa** é a **primeira trilha** da plataforma. Ela demonstra o ciclo completo do
Comunidade Game — mestre publica a trilha → jogador constrói algo real → aprende conceitos →
pontua e ganha visibilidade — e é também a base tecnológica do
[Onboarding por voz](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença).

## 1. O que o jogador faz

Aprender a programar **construindo o próprio robô**:

1. **Monta o corpo** do robô humanoide com material reciclado (garrafa PET) ou kit em MDF.
2. **Personaliza** o robô (nome, pintura, acabamento).
3. **Dá vida ao robô** apontando o smartphone/tablet para o "peito" do boneco: o Web App é
   o **cérebro** — ouve, pensa e fala.
4. **Conversa com o robô**: quiz gamificado sobre programação, explicação de conceitos,
   apoio às atividades escolares.

Habilidades trabalhadas: coordenação motora, criatividade, reuso de materiais
(sustentabilidade), lógica de programação, noções de IA generativa e de nuvem.

## 2. Por que é a primeira trilha

| Critério | Como o Robô Educa atende |
|---|---|
| Baixa barreira de entrada | Não exige computador nem kit caro — garrafa PET + qualquer smartphone |
| Inclusão | Interação por **áudio**, acessível inclusive a pessoas com deficiência visual e a quem ainda não lê com fluência |
| Resultado tangível no 1º dia | O jogador sai com um robô montado e funcionando |
| Faixa 6 a 16 anos | Níveis de dificuldade graduais: da montagem física até a leitura e alteração do código |
| Reaproveitamento | A plataforma já existe e está em produção; serve de base para o Onboarding e para o "converse com seu robô" |

## 3. Anatomia da trilha

### 👤 CORPO — montagem física
Robô humanoide em garrafa PET ou MDF. Atividade presencial de oficina, com material de
baixo custo fornecido por mestres/apoiadores (regra de lastro em
[04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).

> **Lastro já disponível:** o **Goethe-Institut doou 30 kits em MDF** para esta trilha
> ([02 §3](02-conceito-do-jogo-e-gamificacao.md#os-30-kits-em-mdf)). São 30 montagens em MDF
> garantidas; esgotado o estoque, a oficina volta ao material reciclado — que é, de todo
> modo, a versão de menor barreira de entrada e a que ensina reuso.

### 🧠 CÉREBRO — o Web App
Aplicação web acessível por qualquer smartphone, que dá ao robô funções cognitivas:
**ouvir, pensar e falar**.

| Função | Tecnologia |
|---|---|
| Ouvir | `navigator.mediaDevices.getUserMedia` + `SpeechRecognition` (pt-BR, modo contínuo) |
| Falar | `SpeechSynthesisUtterance` (síntese de fala no próprio dispositivo) |
| Pensar | API de IA generativa com *system instructions* (Zero-Shot Prompting) |
| Lembrar | Histórico de conversa persistido por usuário, usado para contextualizar cada resposta |

Arquitetura de referência: backend Python/Flask no padrão **Service/Repository**, banco
NoSQL para o histórico de mensagens, hospedagem em nuvem gerenciada.

### 🛡️ Segurança do conteúdo para crianças
Requisito **obrigatório** desta e de qualquer atividade com IA na plataforma: filtros de
segurança do modelo ativos no nível mais restritivo, bloqueando assédio, discurso de ódio,
conteúdo sexual e conteúdo perigoso. O histórico persistido permite **moderação e controle
de qualidade** das conversas.

## 4. Pontos da trilha (Poder da IA e Robótica)

Decomposição sugerida em pontos de trilha, cada um com desafio de desbloqueio:

1. Montagem do corpo (reuso de materiais, coordenação motora).
2. O que é um assistente de voz — ouvir, pensar, falar.
3. Primeiro quiz com o robô (uso guiado).
4. O que é um *prompt* e como ele muda as respostas do robô.
5. Limites e riscos da IA — alucinação, viés, dados pessoais (letramento crítico).
6. Ler e alterar um trecho de código do robô.
7. **Coleta de dados da sua comunidade pelo robô** — desafio obrigatório de toda trilha
   ([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)):
   o jogador escolhe o que medir no seu território, define com o Mestre a cadência e passa a
   registrar por voz. Enquanto mantiver a série, continua pontuando.
8. Publicar sua versão do robô e apresentá-la aos colegas (culminância).

## 5. Ganchos com a plataforma

- **Onboarding**: o mesmo motor de voz (mediaDevices + reconhecimento + síntese + IA)
  sustenta a tela de cadastro e registro de presença
  ([03 §3](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença)).
- **Apoio às atividades escolares**: o robô é o canal do "peça ajuda para a lição de casa"
  previsto na área do jogador.
- **Comunidades Virtuais**: por voz, o jogador pode registrar dados do território
  (temperatura, ocorrências, resíduos) sem precisar digitar
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)). Como **toda trilha
  precisa ter desafios de coleta de dados reais**
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)),
  o registro por voz é o caminho mais acessível para o jogador que ainda não lê com fluência
  manter uma **série de coleta ativa** — e a série ativa é o que rende pontos de forma
  recorrente.
- **Lançamento automático de pontos**: a conclusão de um quiz pode lançar a atividade
  realizada na API do Comunidade Game.

## 6. Impacto já comprovado

O trabalho de oficinas de inclusão digital com o Robô Educa acontece de forma voluntária
desde **2018** e já impactou centenas de crianças em comunidades de **Salvador, Bahia**.
É a evidência prática de que o modelo funciona antes mesmo da plataforma completa existir —
e o artefato que comprova a habilidade do **Mestre fundador** em Programação e Robótica
([01 §7](01-visao-valores-e-proposito.md#7-o-fundador-primeiro-admin-e-primeiro-mestre)).

## 7. Pontos a definir

- Roteiro pedagógico oficial da oficina (duração, materiais por turma, passo a passo).
- Custo por kit (PET x MDF) para entrar no orçamento de lastro da atividade.
- Integração técnica entre o app do Robô Educa e a API do Comunidade Game
  (autenticação do jogador e lançamento de pontuação).
- Política de retenção do histórico de conversas de menores (LGPD).

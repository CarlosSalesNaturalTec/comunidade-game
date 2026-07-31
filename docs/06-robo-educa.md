# 06 — Trilha Robô Educa (1ª trilha — Poder da IA e Robótica)

> **Autoria:** Mestre fundador. É a **primeira trilha** da plataforma e também a base técnica
> da **App 02 — Assistente por voz e Modo Ouvinte**.

O Robô Educa demonstra o ciclo completo do Comunidade Game — mestre publica a trilha → jogador
constrói algo real → aprende conceitos → pontua e ganha visibilidade — e é a base tecnológica
do onboarding por voz.

## 1. O que o jogador faz

Aprender a programar **construindo o próprio robô**:

1. **Monta o corpo** do robô humanoide com material reciclado (garrafa PET) ou kit em MDF.
2. **Personaliza** o robô (nome, pintura, acabamento).
3. **Dá vida ao robô** apontando o smartphone ou tablet para o "peito" do boneco: o Web App é
   o **cérebro** — ouve, pensa e fala.
4. **Conversa com o robô**: quiz gamificado sobre programação, explicação de conceitos, apoio
   às atividades escolares.

Habilidades trabalhadas: coordenação motora, criatividade, reuso de materiais, lógica de
programação, noções de IA generativa e de nuvem.

## 2. Por que é a primeira trilha

| Critério                     | Como o Robô Educa atende                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Baixa barreira de entrada    | Não exige computador nem kit caro — garrafa PET + qualquer smartphone                                              |
| Inclusão                     | Interação por **áudio**, acessível a pessoas com deficiência visual e a quem ainda não lê com fluência             |
| Resultado tangível no 1º dia | O jogador sai com um robô montado e funcionando                                                                    |
| Faixa 6 a 16 anos            | Níveis graduais, da montagem física à alteração do código; nas equipes mistas, os mais velhos apoiam os mais novos |
| Reaproveitamento             | A plataforma já existe e está em produção; serve de base para o onboarding e para o "converse com seu robô"        |

## 3. Anatomia da trilha

### 👤 CORPO — montagem física

Robô humanoide em garrafa PET ou MDF. Atividade presencial de oficina, com material de baixo
custo fornecido por mestres ou apoiadores.

> **Lastro já disponível:** os **30 kits em MDF** doados pelo Goethe-Institut garantem 30
> montagens em MDF; esgotado o estoque, a oficina volta ao material reciclado — que é, de todo
> modo, a versão de menor barreira de entrada e a que ensina reuso.

### 🧠 CÉREBRO — o Web App

Aplicação web acessível por qualquer smartphone, que dá ao robô funções cognitivas: **ouvir,
pensar e falar**.

| Função  | Tecnologia                                                                            |
| ------- | ------------------------------------------------------------------------------------- |
| Ouvir   | `navigator.mediaDevices.getUserMedia` + `SpeechRecognition` (pt-BR, modo contínuo)    |
| Falar   | `SpeechSynthesisUtterance` (síntese no próprio dispositivo)                           |
| Pensar  | API de IA generativa com _system instructions_ (Zero-Shot Prompting)                  |
| Lembrar | Histórico de conversa persistido por usuário, usado para contextualizar cada resposta |

Arquitetura de referência: backend Python/Flask no padrão **Service/Repository**, banco NoSQL
para o histórico de mensagens, hospedagem em nuvem gerenciada.

### 🛡️ Segurança do conteúdo para crianças

Requisito **obrigatório** desta e de qualquer atividade com IA na plataforma: filtros de
segurança do modelo no nível mais restritivo, bloqueando assédio, discurso de ódio, conteúdo
sexual e conteúdo perigoso. O histórico persistido permite **moderação e controle de
qualidade** das conversas.

## 4. Pontos da trilha

Decomposição sugerida, cada ponto com desafio de desbloqueio:

1. Montagem do corpo (reuso de materiais, coordenação motora).
2. O que é um assistente de voz — ouvir, pensar, falar.
3. Primeiro quiz com o robô (uso guiado).
4. O que é um _prompt_ e como ele muda as respostas do robô.
5. Limites e riscos da IA — alucinação, viés, dados pessoais (letramento crítico).
6. Ler e alterar um trecho de código do robô.
7. **Coleta de dados da sua comunidade pelo robô** — o desafio de coleta obrigatório de toda
   trilha: o jogador escolhe o que medir no seu território, define com o Mestre a cadência e
   passa a registrar por voz. Enquanto mantiver a série, continua pontuando.
8. **Publicar sua versão do robô e apresentá-la aos colegas** — a **criação original** desta
   trilha: seu robô, seu nome, sua pintura, suas alterações de código, com autoria creditada e
   lugar no portfólio público.

Os títulos de **Mecânica** e **Programação** do acervo Include são a bibliografia de apoio
desta trilha (documento 05).

## 5. Ganchos com a plataforma

- **Onboarding**: o mesmo motor de voz sustenta a tela de cadastro e registro de presença.
- **Apoio às atividades escolares**: o robô é o canal do "peça ajuda para a lição de casa".
- **Comunidades Virtuais**: por voz, o jogador registra dados do território sem precisar
  digitar — o caminho mais acessível para quem ainda não lê com fluência manter uma **série de
  coleta ativa**, que é o que rende pontos de forma recorrente.
- **Lançamento automático de pontos**: a conclusão de um quiz pode lançar a atividade
  realizada na API da plataforma.

## 6. Impacto já comprovado

As oficinas de inclusão digital com o Robô Educa acontecem de forma voluntária desde **2018** e
já impactaram centenas de crianças em comunidades de **Salvador (BA)**. É a evidência prática
de que o modelo funciona antes mesmo de a plataforma completa existir — e o artefato que
comprova a habilidade do Mestre fundador em Programação e Robótica.

## 7. Pontos a definir

- Roteiro pedagógico oficial da oficina (duração, materiais por turma, passo a passo).
- Custo por kit (PET × MDF) para entrar no orçamento de lastro da atividade.
- Integração técnica entre o app do Robô Educa e a API do Comunidade Game (autenticação do
  jogador e lançamento de pontuação).
- Política de retenção do histórico de conversas de menores (LGPD).

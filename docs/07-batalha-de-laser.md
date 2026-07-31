# 07 — Trilha Batalha de Laser (2ª trilha — Poder da IA e Robótica)

> **Autoria:** Mestre fundador. Sucessora natural do Robô Educa, com um degrau a mais de
> complexidade: eletrônica, sensores e rede. Os jogadores constroem os artefatos, aprendem os
> conceitos e disputam a **Batalha** presencial — fechando o ciclo aprender → construir →
> batalhar → pontuar.
>
> Os títulos de **Eletrônica** e **Sensores** do acervo Include são a bibliografia de apoio
> desta trilha (documento 05).

## 🌌 Os 4 elementos do jogo

### 1. O Atacante (Guerreiro / classe Dano)

- **Arma:** artefato com emissor laser.
- **Energia (stamina):** o atacante não atira infinitamente. Parte de 100%; cada tiro gasta um
  pouco. Em 0% a arma "trava" (superaquecimento) e leva alguns segundos para recarregar.
- **Comunicação:** o NodeMCU publica via Wi-Fi/MQTT o nível de stamina a cada tiro e a cada
  recarga — apenas telemetria.

### 2. O Defensor (Paladino / classe Tanque)

- **Arma:** "Escudo de Luz" com NodeMCU, **2 LDRs** e fita de **5 LEDs**.
- **Defesa:** o Defensor se joga na frente dos lasers para proteger a torre. Cada acerto no
  sensor apaga um LED. A detecção de hit roda **localmente**, sem depender da rede.
- **Exaustão:** com 0 LEDs o escudo "quebra"; o Defensor deve dar espaço ao Atacante até a
  energia reiniciar.
- **Comunicação:** publica seu HP e avisa quando recarrega. Em caso de penalidade, publica um
  evento especial que a Torre escuta pelo broker.

### 3. A Torre (a grande base)

- **Hardware:** NodeMCU + fita de **30 LEDs** em disposição circular + **2 LDRs** + DFPlayer
  Mini (caixa de som).
- **Alvo:** coração da equipe, inicia com 100% de vida. Tiro que passa pelo escudo e acerta a
  torre causa dano simples, detectado diretamente pelo LDR. A lógica roda local; o resultado é
  publicado via MQTT.
- **Comunicação:** publica sua vida e assina o tópico de penalidade do Defensor para aplicar
  Dano Duplo quando necessário.

### 4. O Nexus (estação de controle / o Mestre)

- **Hardware:** notebook do Controlador, na mesma rede Wi-Fi dos NodeMCUs.
- **Broker MQTT:** **Mosquitto** rodando localmente — sem depender de internet.
- **Roteador:** **TP-Link dedicado ao jogo** (rede isolada), o que garante estabilidade
  independentemente do ambiente do evento.
- **Painel:** aplicação Python que assina `game/#` e exibe em tempo real a energia do Ataque, a
  resistência do Defensor e o HP da Torre, com animações.
- **Estatísticas:** MVP, tiros acertados, quebras de escudo e penalidades ao fim de cada
  partida.

## 📡 Arquitetura de comunicação

> **Decisão de projeto:** o laser atingindo o LDR é sempre o gatilho real do jogo. A rede
> Wi-Fi serve **exclusivamente como telemetria**.

```text
[Atacante NodeMCU]  ─────────────────────────────┐
[Defensor NodeMCU]  ──── Wi-Fi / MQTT ────────────┼──► [TP-Link Dedicado] ──► [Notebook/Nexus]
[Torre NodeMCU]     ─────────────────────────────┘      Broker: Mosquitto
```

| Componente | Tópico                  | Payload exemplo                      |
| ---------- | ----------------------- | ------------------------------------ |
| Atacante   | `game/atacante/stamina` | `{"stamina": 75, "status": "ativo"}` |
| Defensor   | `game/defensor/hp`      | `{"hp": 3, "status": "ativo"}`       |
| Defensor   | `game/defensor/punicao` | `{"tipo": "DANO_DUPLO"}`             |
| Torre      | `game/torre/hp`         | `{"hp": 60}`                         |
| Nexus      | `game/nexus/comando`    | `{"cmd": "START"}`                   |

**Fluxo da penalidade de Dano Duplo:** escudo com HP 0 detecta hit no LDR → publica
`game/defensor/punicao` → a Torre, assinante do tópico, aplica dano × 2 localmente → publica
seu novo HP → o Nexus exibe alarme visual e aciona o som de explosão. O delay de ~20 ms é
imperceptível.

**Roteador em modo isolado:** SSID `GAME_NEXUS`, DHCP em `192.168.1.x`, sem internet, broker
Mosquitto no IP fixo `192.168.1.100` (o notebook).

## 📜 Regras do campo de batalha

1. **Gestão de energia.** O poder no jogo é fluido: atacante e defensor não "morrem" — suas
   baterias se esgotam e se renovam sozinhas em alguns segundos. Cabe às equipes entrar em
   sintonia: o Atacante deve atirar quando o escudo cair, sem gastar munição atirando nas
   paredes.
2. **A hitbox perfeita.** Os tiros só valem se o laser incidir precisamente nos LDRs, detectado
   localmente. Valem tiros diretos.
3. **Penalidade severa (falta técnica).** O Defensor com escudo esgotado está imobilizado e não
   pode proteger a torre até os 5 LEDs reacenderem. Se o Atacante acertar o LDR do escudo
   descarregado porque o defensor insistiu em fazer "parede humana", o escudo publica o evento
   de penalidade e a Torre **aplica Dano Duplo imediatamente**. A lição prática: posicionamento
   estratégico, ética no esporte e limites de sistema — sobrecarregar um sistema já sem energia
   explode algo maior.
4. **Vitória.** O jogo não termina por tempo: termina quando a energia vital da Torre adversária
   chega a 0%.

## 🎭 A partida

- **Pre-game.** O Controlador aciona "Start" no painel; o Nexus publica `{"cmd": "START"}`. As
  30 luzes da Torre acendem, o DFPlayer anuncia _"Batalha iniciada! Protejam a base."_ e os
  escudos acendem os 5 LEDs em azul.
- **Mid-game.** O Atacante avança disparando; o Defensor se coloca na frente. Cada impacto
  absorvido apaga um LED do escudo e é registrado no painel. Rajadas rápidas demais fazem a
  arma "engasgar": stamina 0, luz vermelha piscando e aviso de reinicialização de energia.
- **Punição.** Escudo em HP 0, controlador avisa _"Escudo quebrado! Sai da frente!"_. Se o
  defensor não recua e o laser acerta, o alarme dispara, os 30 LEDs da torre piscam em vermelho
  e soa a explosão: **dano duplo aplicado**.
- **Game over e telemetria.** A torre zera, o Nexus pausa o sistema e exibe o resumo da partida
  no telão — tiros dados, reinicializações de energia, defesas corretas, quebras de escudo e
  penalidades cometidas.

## 🛠️ Visão do Mestre — a lógica de programação

> **Princípio central: toda lógica de jogo roda localmente em cada NodeMCU. A rede é
> exclusivamente telemetria.**

```cpp
// Defensor (escudo)
void loop() {
  if (analogRead(LDR) < LIMIAR_HIT) {   // laser detectado localmente
    if (hpEscudo > 0) {
      hpEscudo--;
      atualizarLEDs();
      mqtt.publish("game/defensor/hp", hpEscudo);
    } else {                            // escudo já zerado → penalidade
      mqtt.publish("game/defensor/punicao", "DANO_DUPLO");
    }
  }
  if (hpEscudo == 0) {
    delay(TEMPO_RECARGA);               // recarga local, sem rede
    hpEscudo = 5;
    atualizarLEDs();
    mqtt.publish("game/defensor/hp", 5);
  }
}

// Torre — assinante do tópico de penalidade
void onMqttMessage(topic, payload) {
  if (topic == "game/defensor/punicao") vidaTorre -= (danoLaser * 2);
  if (topic == "game/nexus/comando" && payload == "START") iniciarPartida();
  mqtt.publish("game/torre/hp", vidaTorre);
}
```

O painel do Nexus é uma aplicação Python com `paho-mqtt` que assina `game/#` e atualiza as
barras de HP e stamina conforme as mensagens chegam, disparando alarme visual e sonoro no
tópico de punição.

## 📦 Hardware do projeto

| Componente | Hardware                                                | Qtd |
| ---------- | ------------------------------------------------------- | --- |
| Atacante   | NodeMCU ESP8266 + módulo laser                          | 1   |
| Defensor   | NodeMCU ESP8266 + 2× LDR + fita 5 LEDs                  | 1   |
| Torre      | NodeMCU ESP8266 + 2× LDR + fita 30 LEDs + DFPlayer Mini | 1   |
| Nexus      | Notebook (Python + Mosquitto MQTT)                      | 1   |
| Roteador   | TP-Link TD-VG5611 (rede isolada)                        | 1   |

## Integração com a plataforma **[Proposta]**

- **Segurança do laser**: documentar a classe do laser utilizada e as regras de segurança
  ocular (nunca apontar para o rosto; preferir módulos de baixa potência, classe 1 ou 2) —
  requisito para atividade com crianças.
- **Ponte Nexus → API**: ao fim da partida, o Nexus envia as estatísticas (MVP, tiros, defesas,
  penalidades) para a API, lançando automaticamente a atividade realizada e os pontos — a
  primeira integração real entre uma batalha física e o backend.
- **Trilha associada**: decompor a construção dos artefatos em pontos de trilha (eletrônica
  básica → LDR e LEDs → Wi-Fi/MQTT → lógica do jogo → dashboard Python), cada um com desafio de
  desbloqueio.
- **Desafio de coleta de dados** — obrigatório em toda trilha, e aqui o encaixe é direto: o
  mesmo **LDR** que detecta o laser mede **luminosidade**, e o NodeMCU que publica telemetria
  publica igualmente uma leitura de sensor. A trilha pode terminar com o jogador instalando um
  **sensor de território** — iluminação pública, temperatura, chuva — construído por ele e
  alimentando a série temporal da sua Comunidade Virtual.
- **Protagonismo na batalha**: variações de regra propostas pelos próprios jogadores (novos
  modos de partida, penalidades, tempos), avaliadas pelo Mestre antes de valerem em campo;
  artefatos personalizados — pintura, carcaça, nomes — como **criação original** da trilha; e
  papéis de equipe que misturam idades, com os mais velhos operando o que exige mais cuidado
  (laser, Nexus) e apoiando os mais novos.

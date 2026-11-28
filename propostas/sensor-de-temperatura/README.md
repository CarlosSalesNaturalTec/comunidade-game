# Sensor de temperatura do território — proposta

`[Proposta]` — material ainda **não decidido** pelo fundador. Não é código de change do
OpenSpec: vira implementação só depois das decisões abaixo, pelo fluxo do `CLAUDE.md`
(documento-fonte → documento 09 → PRD → change).

## Conteúdo

| Arquivo                                      | O que é                                                   |
| -------------------------------------------- | --------------------------------------------------------- |
| `firmware/sensor-de-temperatura/`            | Programa do ESP32 (Arduino IDE); o aluno preenche o Wi-Fi |
| `guia-de-montagem-sensor-de-temperatura.pdf` | Guia ilustrado: materiais, ligação, abrigo, instalação    |

O firmware usa o contrato já implementado: `POST /v1/registros-de-coleta` com origem `sensor`,
autenticado pelos cabeçalhos `X-Chave-Aplicacao` e `X-Credencial-Dispositivo`
(`identificador.segredo`). Ainda não foi compilado nem testado em placa.

## Decisões pendentes

1. Pasta definitiva do firmware no repositório (documento 03 §1.2) e a esteira de CI dela.
2. Tela na App 09 que emite a credencial e entrega o `config.h` preenchido, ou preenchimento
   manual pelo Mestre.
3. Qual chave de aplicação o sensor usa.
4. Trilha em que o sensor é construído: Mapa Vivo ou Batalha de Laser.
5. Intervalo de medição padrão (proposto: 30 minutos).

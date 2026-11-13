## ADDED Requirements

### Requirement: A camada comum entrega o registro da customização do kit

A camada comum SHALL entregar o **registro da customização do kit** feito pelo próprio
Guerreiro(a): a descrição por voz ou texto, a foto ou o vídeo só do kit, o aviso e o envio
retomável com progresso. As aplicações em que a criança registra a customização — a App 05 em
casa e, na fatia 35 do PRD-04, a App 01 no encontro — SHALL consumir este mesmo registro, e
NEVER SHALL manter cópia própria dele. A captura na hora pelo Mestre (`RF-04-82`) não é este
registro. (`RF-05-102`, `RF-04-80`)

O aviso SHALL dizer, com estas palavras: "Foto ou vídeo só do kit, sem o seu rosto. Se o
Mestre aprovar no encontro, o registro fica guardado no seu acervo e pode ir à vitrine, com o
seu nick, se o seu responsável autorizar." — e SHALL oferecer o **Saber mais**, no molde do
aviso da comprovação do prático. (texto aprovado pelo fundador em 2026-11-13, PRD-05 §11)

#### Scenario: O aviso sai com o texto aprovado

- **WHEN** o registro da customização é apresentado
- **THEN** o aviso traz o texto aprovado e o Saber mais, antes do controle de envio

#### Scenario: O formato aceito é foto ou vídeo

- **WHEN** a criança escolhe o arquivo do registro
- **THEN** o seletor oferece só imagem e vídeo

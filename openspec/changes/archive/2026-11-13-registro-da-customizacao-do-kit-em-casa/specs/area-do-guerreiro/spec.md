## ADDED Requirements

### Requirement: A lista de conquistas abre o registro da customização do kit

Na lista de conquistas, a recompensa que é **kit com customização aberta** para o Guerreiro(a)
em sessão SHALL mostrar, no próprio cartão, a situação do último registro dele e a ação que
cabe; a recompensa cuja customização não abriu SHALL continuar como antes, sem ação nova. O
registro NEVER SHALL ganhar aba nem caminho próprio na Área do Guerreiro(a). (`RF-05-102`,
`RF-05-103`, resposta do fundador de 2026-11-13)

| Último registro do kit                   | O cartão mostra                                            |
| ---------------------------------------- | ---------------------------------------------------------- |
| nenhum, cancelado ou expirado            | Registrar a customização                                   |
| pendente, sem a mídia recebida           | retomar o envio da foto ou do vídeo do mesmo registro      |
| pendente, com a mídia recebida           | aguardando a aula, o aviso de que expira no fim do ciclo e Cancelar |
| reprovado                                | o motivo do Mestre e Enviar de novo                        |
| aprovado                                 | aprovado, e Registrar a customização para uma nova         |

#### Scenario: Kit aberto oferece o registro

- **WHEN** o Guerreiro(a) abre a lista de conquistas e um kit recebido tem a customização
  aberta, sem registro
- **THEN** o cartão daquele kit oferece Registrar a customização

#### Scenario: Recompensa sem customização aberta não muda

- **WHEN** a recompensa não é kit aberto — livro, camisa, ou kit cujo prático ainda não foi
  aprovado
- **THEN** o cartão mostra só o que já mostrava, sem ação de customização

#### Scenario: O pendente aguarda a aula e se cancela

- **WHEN** o kit tem registro pendente com a mídia recebida
- **THEN** o cartão diz que aguarda a aula e que expira no fim do ciclo, e oferece Cancelar
- **AND WHEN** o Guerreiro(a) cancela
- **THEN** o cartão volta a oferecer Registrar a customização

#### Scenario: O reprovado mostra o motivo e se reenvia

- **WHEN** o último registro do kit foi reprovado
- **THEN** o cartão mostra o motivo escrito pelo Mestre e oferece Enviar de novo, que abre um
  registro novo

### Requirement: O registro em casa leva a mídia só do kit e a descrição

O registro SHALL pedir a **descrição** da customização, por **voz ou texto** — a fala é
transcrita no aparelho e cai no campo, editável, e ao núcleo vai só o texto —, e a **foto ou o
vídeo só do kit, sem rosto**. O **aviso** SHALL vir **antes** do controle de envio, nunca
depois. O controle de registrar SHALL ficar indisponível enquanto faltar a descrição ou a
mídia. O envio SHALL mostrar o **progresso** e, caindo a rede, SHALL dizê-lo e oferecer retomar
o envio do **mesmo** registro, sem criar outro. Sem transcrição de fala no aparelho, o registro
SHALL seguir só por texto. A recusa do núcleo SHALL aparecer em linguagem simples.
(`RF-05-102`, PRD-05 §11)

#### Scenario: O aviso vem antes do envio

- **WHEN** o Guerreiro(a) abre o registro de um kit
- **THEN** o aviso aparece antes do controle de escolher a foto ou o vídeo

#### Scenario: Falta a descrição ou a mídia

- **WHEN** a descrição está em branco ou nenhuma foto ou vídeo foi escolhido
- **THEN** o controle de registrar fica indisponível

#### Scenario: A fala cai no campo da descrição

- **WHEN** o Guerreiro(a) fala a descrição num aparelho que transcreve
- **THEN** a transcrição aparece no campo, editável, e é ela que vai ao núcleo

#### Scenario: A rede cai no meio do envio

- **WHEN** a conexão cai durante o envio da mídia de um registro já gravado
- **THEN** a tela diz que a conexão caiu e oferece retomar, e retomar envia ao mesmo registro

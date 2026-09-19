## Context

A bancada (`openspec/specs/aplicacao-da-aula-presencial`, Requirement "O Mestre mede no aparelho
a distância entre descritores") já captura, compara e apresenta a distância na unidade do núcleo.
A comparação do núcleo (`backend/src/nucleo/biometria/regra.py`,
`autenticar_por_nick_e_descritor`) já calcula a mesma distância e a confronta com um limiar. O
que esta fatia decide é **onde o limiar mora**, **como ele nasce** e **o que acontece sem ele**.

`Aula.ponto_de_apoio_id` é obrigatório, e as duas portas da App 01 que abrem a bancada — o
caminho do diagnóstico e o do onboarding — correm dentro de uma sessão de trabalho que já
conhece a aula. O ponto de apoio, portanto, é sempre determinável nas duas pontas.

## Decisions

1. **O limiar é dado do ponto de apoio, gravado por medição, e o ambiente deixa de declará-lo.**
   `CG_BIOMETRIA_LIMIAR_DE_COMPARACAO` sai da `Configuracao`. Um ponto de apoio sem medição não
   reconhece ninguém (`RF-01-73`, decisão do fundador, 2026-09-18).

   Descartada: manter a variável como padrão e deixar o banco sobrepor. Nunca ficaria sem
   limiar, e é exatamente o que mascara o defeito de hoje — o valor errado do ambiente seguiria
   servindo, silenciosamente, a todo ponto de apoio que ninguém mediu.

   Descartada: um limiar global no banco, semeado na migração. Troca o segredo por uma linha de
   tabela e mantém o problema de fundo — um número só para salas com câmeras e luzes diferentes.

2. **A ausência de limiar não é silenciosa, porque a gestão a mostra.** É a contrapartida da
   decisão 1: a recusa em si é indistinguível, como o `RN-01-22` exige, mas a área Pontos de
   Apoio lista quem não tem limiar medido (`RF-02-109`). Sem isso, a decisão 1 criaria a quarta
   falha silenciosa deste mesmo caminho, depois do 422 da dimensão, do CORS do bucket e do
   backend autosselecionado da Human.

3. **A gravação vai autenticada pela sessão de trabalho; a leitura resolve o ponto de apoio pela
   aula.** Gravar exige Mestre ou Admin pela matriz (`RF-01-16`) e carrega a aula em curso. Ler
   acontece em `POST /v1/sessoes/guerreiro`, que é pública quanto à persona (`RF-01-04`) e não
   pode ganhar credencial: ela passa a receber a **aula**, e o núcleo confere que a aula está
   vigente e que o vínculo do Guerreiro(a) é da comunidade dela — o mesmo laço que
   `registrar_presenca` já aplica. Quem escolher uma aula alheia não alcança limiar de outra
   comunidade, e qualquer falha dessa conferência cai na recusa única do `RN-01-22`.

   Descartada: deduzir o ponto de apoio da comunidade do Guerreiro(a). Uma comunidade pode ter
   mais de um ponto de apoio, e a dedução seria ambígua justamente onde o valor difere.

   Descartada: exigir o token da sessão de trabalho na rota de reconhecimento. Fecharia o
   contorno por completo, e contraria o `RF-01-04`, que é regra de produto — se for para mudar,
   muda no PRD, não aqui.

4. **A medição é a unidade gravada, e o limiar vigente é a medição mais recente do ponto de
   apoio.** Uma tabela só: ponto de apoio, o limiar, as duas séries de distâncias, quem mediu e
   quando. O histórico sai de graça, a medição suspeita pode ser reexaminada, e não há um segundo
   registro "vigente" para sair de sincronia com o primeiro (`RF-01-73`, `RF-02-109`).

5. **O que trafega são distâncias e o número — nunca descritor nem imagem.** O documento 03 §3.3
   já dizia que "o que se registra é a distância, nunca o descritor"; o que muda é a frase
   seguinte, "nada envia ao núcleo", que passa a valer para descritor e imagem. A regra do
   `RN-04-32` — um descritor de referência por vez, comparada descartada no ato — não muda:
   nenhum descritor sobrevive à comparação, e portanto nenhum pode ser enviado.

6. **O valor proposto é o ponto médio entre o maior piso e o menor teto** (decisão do fundador,
   2026-09-18): a escolha equidistante das duas formas de errar — recusar quem é e aceitar quem
   não é. A bancada propõe; Mestre ou Admin confirma, e a gravação registra quem confirmou.

   Descartada: propor mais perto do piso, privilegiando a recusa. Mais seguro, e devolve à
   confirmação humana um volume que a decisão de calibrar existia justamente para reduzir.

7. **Séries que se sobrepõem não gravam.** Se o maior piso alcança o menor teto, não existe
   limiar que acerte os dois lados, e gravar um número ali seria gravar um erro. A tela diz que
   não há limiar viável e pede nova medição (`RN-04-35`). É a única saída que preserva o sentido
   da calibração — e, quando acontecer, o que ela está dizendo é que as capturas daquela sala
   não separam pessoas, que é informação mais útil que um número.

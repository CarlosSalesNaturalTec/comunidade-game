## Context

Fatia só de tela. `GET /v1/vitrine/necessidades` já existe, pública e sem credencial de persona,
e devolve por necessidade o tipo de recurso com nome, a quantidade faltante, o valor em moedas
(ou `null`, quando o tipo não tem vigência de referência), a comunidade, o ponto de apoio e o
início e o fim da aula (`necessidade-de-recurso`). A chave PIX chega pela leitura de
`conteudo-institucional` que a fatia 5 montou, memorizada em memória por carga de página. A porta
de pré-cadastro da App 08 existe (`area-do-apoiador`) e recebe apenas o link de saída. Os padrões
de endereço próprio, de leitura com estado e de "nada no aparelho" já estão em
`aplicacao-da-vitrine`. Nenhuma mudança no núcleo.

## Decisions

1. **A porta é tela da vitrine, em `/quero-participar`** — não um link direto para a App 08. É o
   que põe a chave PIX e as necessidades **dentro da porta**, como o `RF-03-43` exige: as duas
   são leitura da vitrine, e a App 08 não as tem. A porta termina em link de saída para o
   pré-cadastro da App 08 (decisão do fundador, 2026-09-29). Alternativa descartada: chamada
   apontando direto para a App 08 — deixaria o `RF-03-43` sem lugar.
2. **O garfo de modalidade só encaminha.** A porta nomeia as sete respostas do documento 14 §10
   com o comprobatório de cada uma e leva a um dos dois destinos que já existem — o pré-cadastro
   da App 08 ou `/participar`. Nenhum campo novo no formulário e nenhum atributo novo em
   `SolicitacaoDeParticipacao`: quem traz material, serviço, conteúdo, código, divulgação ou quer
   ensinar descreve isso na apresentação e nos links comprobatórios que o `RF-03-28` já aceita
   (decisão do fundador, 2026-09-29). Alternativa descartada: gravar a modalidade — leva campo,
   migração e mudança no PRD-01 §8, fora do recorte desta fatia.
3. **A porta não recebe nada de quem estava sendo visto.** O componente da porta **não tem
   propriedade de origem** e o endereço `/quero-participar` não tem parâmetro — o `RF-03-41` e o
   `RN-03-25` ficam garantidos por construção, não por cuidado de redação. A chamada é o mesmo
   componente em toda página individual, e ele só chama `irPara`.
4. **A saída da recusa usa o voltar do navegador.** `useNavegacao` ganha `voltar()`, que chama
   `history.back()` quando esta carga já empilhou algum endereço e cai em `irPara("/")` quando a
   porta foi aberta por endereço direto. O que sabe se houve empilhamento é contador **em
   memória** do próprio hook, que morre na recarga — nada vai ao aparelho (`RF-03-38`,
   `RN-03-15`). Alternativa descartada: voltar sempre à raiz — perderia a página que o visitante
   estava lendo.
5. **Uma leitura de necessidades por carga**, memorizada em memória no padrão de
   `useConteudoInstitucional`, compartilhada pela porta e pelo bloco de "Como apoiar"; a porta
   reaproveita a leitura institucional já memorizada para a chave PIX, sem consulta nova.
6. **A lista de necessidades é lista, não tabela.** Sete campos por necessidade não cabem em
   tabela no celular, e a vitrine é Mobile First (documento 03 §1.1): cada necessidade sai como
   item com rótulo e valor. Necessidade sem valor em moedas sai com a falta e sem o valor — a
   aplicação nunca arbitra número (`RN-03-18`).
7. **A chamada entra nas páginas que existem.** `PaginaDoGuerreiro` já recebe `irPara`;
   `PaginaDaComunidade` passa a receber. As páginas de Mestre e de Apoiador da fatia 7 reusam o
   mesmo componente, e a seção de poderes segue sem página individual — o `RF-03-39` sai parcial
   na linha do cronograma (decisão do fundador, 2026-09-29).
8. **"Como apoiar" troca a frase pendente pelo bloco de necessidades**, no lugar onde a fatia 5
   a deixou anotada.

## Risks / Trade-offs

- A chave PIX passa a aparecer em duas telas — "Como apoiar" e a porta: o valor continua vindo
  só do núcleo, e nenhuma cópia é escrita na aplicação.
- A chamada em toda página individual aumenta o peso da página do Guerreiro(a), que já carrega a
  carta inteira: o componente é texto e dois botões, sem leitura nova.
- `semRastro.test.tsx` cobre a visita inteira sem gravação; a ação de acompanhar entra nessa
  cobertura, e não em teste próprio de armazenamento.

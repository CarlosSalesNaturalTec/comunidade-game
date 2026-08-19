## Context

Primeira pasta de código fora de `backend/`. Nada de frontend existe para imitar: esta fatia
funda o padrão que as outras seis aplicações vão repetir, e é por isso que o desenho pesa mais
do que o recorte funcional sugere. Ver `proposal.md` para a motivação.

O que já está decidido e **não se reabre aqui**: React com TypeScript sobre Vite, Astro só na
vitrine, saída estática no Firebase Hosting e a pasta `comum/` na raiz (documento 03 §1);
Biome e Vitest na esteira, com as três verificações bloqueando o merge (documento 09); tokens
em CSS puro, nas camadas semântica e de tema, no temperamento Operação (documento 15 §§6, 12);
origem aberta no núcleo (documento 03 §1, princípio 2).

O contrato do núcleo está pronto e conferido: chave em `X-Chave-Aplicacao`, sessão em
`Authorization: Bearer` com token opaco, `POST /v1/sessoes/social` recebendo o `id_token` do
Google e devolvendo `{ token, expira_em, papel }`, e `POST /v1/comunidades` restrito ao Admin.

## Goals / Non-Goals

**Goals:**

- Fundar a forma de uma aplicação deste repositório: pastas, esteira, cliente de API e
  tratamento das duas credenciais.
- Deixar `comum/` consumível pelas outras sete aplicações e pelo jogo sem reescrita.
- Entregar o cadastro de Comunidade Virtual de ponta a ponta, com as recusas visíveis.

**Non-Goals:**

- Publicar a aplicação em endereço próprio: o documento 03 já diz onde, e o workflow de
  publicação é de outra fatia.
- Biblioteca de componentes ou de gráfico: nenhuma está decidida, e esta fatia não precisa de
  nenhuma.
- A carta do documento 15 §8.1: `comum/` nasce só com os tokens, porque esta fatia não tem
  card. O §12 põe prazo no arquivo de tokens; o §8.1 não põe prazo na carta.
- Estado global no cliente: três telas não justificam.

## Decisions

**`comum/` é pacote de espaço de trabalho, não caminho relativo.** A raiz declara
`workspaces` com `comum`, `apps/*` e `jogos/*`, e cada aplicação depende de `comum` pelo nome.
Alternativa descartada: importar `../../comum/tokens.css` por caminho relativo — funciona no
Vite, mas quebra quando uma aplicação for construída ou publicada isoladamente, que é
exatamente o princípio 3.

**O `package.json` da raiz passa a ser o manifesto do monorepo.** Ele hoje só carrega a
esteira de texto. Alternativa descartada: um segundo manifesto só para JavaScript — dois
`npm install` na preparação do ambiente, sem ganho.

**Biome e Prettier não se sobrepõem.** Biome formata e linta `comum/` e `apps/*`; Prettier
segue dono de `.md` e da configuração da raiz. `.prettierignore` passa a excluir as pastas de
código, e o Biome só enxerga as pastas dele. Alternativa descartada: Biome também no
Markdown — ele não formata Markdown, e a esteira de texto já está estabilizada.

**O token de sessão fica em `sessionStorage`.** Sobrevive ao recarregar a aba e morre quando
ela fecha, que é o comportamento certo para um aparelho que pode ser compartilhado. O token é
opaco e o núcleo já o expira por conta própria. Alternativas descartadas: memória — perde a
sessão a cada recarregamento, penalizando quem opera em pé; `localStorage` — sobrevive ao
fechamento do navegador, o que num aparelho compartilhado é exposição sem contrapartida.

**A recusa da chave e a recusa da sessão são tratadas em separado.** O cliente de API
distingue as duas antes de decidir o que a tela faz: sessão recusada devolve à entrada, chave
recusada é falha de implantação e não se resolve tentando de novo. É o `RN-01-34` chegando à
interface.

**O `id_token` vem do Google Identity Services, carregado do próprio Google.** É a única
dependência externa em tempo de execução da aplicação, e é inevitável: o núcleo confere a
assinatura do token contra o JWKS do Google e a audiência contra `google_client_id`.

**A chave de aplicação e o _client ID_ entram por variável de ambiente do Vite**, uma por
ambiente, como o princípio 2 exige. Ambas terminam no pacote entregue ao navegador — o
desenho já assume isso, porque a chave é da aplicação e não da pessoa.

**O CORS entra como middleware no núcleo**, em `principal.py`, permitindo qualquer origem, os
métodos que as rotas usam e os cabeçalhos `X-Chave-Aplicacao` e `Authorization`, sem
credencial de cookie. Nenhuma rota muda. Alternativa descartada: reescrita no Firebase
Hosting para evitar cross-origin — amarraria os sete frontends ao provedor, contra o
princípio 4.

**Os testes trocam o cliente de API por um duplo.** Vitest cobre o cliente de API — as duas
credenciais e a separação das recusas — e as telas, pelo comportamento que as specs
descrevem. Nenhum teste desta fatia fala com o núcleo de verdade.

## Risks / Trade-offs

**A origem aberta permite que a chave da App 03 seja usada de qualquer página** → é
consequência aceita da decisão do documento 03: CORS não barra chamada feita fora do
navegador, e quem protege é a cota por chave e o freio por origem. A chave é por aplicação e
por ambiente, então o estrago se limita e se revoga.

**`sessionStorage` é alcançável por script na página** → a aplicação não carrega script de
terceiro além do Google Identity Services, e o token é opaco, curto e revogável pelo núcleo.
Cookie `HttpOnly` seria mais forte, mas o núcleo lê a sessão de `Authorization`, e mudar isso
seria alterar o contrato do PRD-01 dentro de uma fatia de frontend.

**Esta fatia funda padrão para outras seis aplicações** → é o risco real do recorte. Mitigação:
tudo que for reaproveitável nasce em `comum/` ou na configuração da raiz, e o que é da App 03
fica na pasta dela.

**A esteira de CI da pasta nasce sem código de outras aplicações para exercitá-la** → o
workflow dispara pelo caminho, e o caminho hoje só tem uma aplicação; quando a segunda nascer,
o mesmo workflow a alcança sem edição.

## Open Questions

- O `.lycheeignore` pode precisar de entrada para `accounts.google.com` se algum `.md` desta
  fatia citar o endereço do Google Identity Services. Resolve-se ao escrever, sem mudar specs
  nem tarefas.

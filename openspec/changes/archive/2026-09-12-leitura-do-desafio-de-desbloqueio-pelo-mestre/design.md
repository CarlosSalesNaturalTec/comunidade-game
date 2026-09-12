## Context

Ver `proposal.md` — Why. O que o desenho precisa considerar:

- `MissaoSaida` é a saída compartilhada por rota pública, leitura de trilha e listagens; a
  decisão 4 da fatia 18 a manteve **sem** os campos do desafio para que a alternativa correta
  não vazasse ao Guerreiro(a). A decisão continua válida.
- `GET /v1/trilhas/minhas` já devolve `MissaoDoMestreSaida`, subclasse de `MissaoSaida`
  exclusiva do Mestre autor, criada pela decisão 1 da fatia 7 justamente para aninhar o que só
  ele pode ver — hoje o desafio de coleta.
- A declaração já monta a saída ao autor: `_saida_das_perguntas` e a composição com
  `alternativa_correta` em `MissaoComDesafioDeDesbloqueioSaida`.
- A rota que serve os bytes da imagem ao autor e ao Guerreiro(a) inscrito já existe (fatia
  19), e a App 05 já tem o componente que a consome.

## Goals / Non-Goals

**Goals:**

- O Mestre autor reabre e corrige o desafio entre sessões, sem reenviar arquivo.
- A alternativa correta continua fora de toda leitura que alcance o Guerreiro(a).
- A sondagem se apresenta pelo que é, sem duplicar a tela do desbloqueio.

**Non-Goals:**

- Rota nova de leitura do desafio. Não se cria porta onde a existente já é do autor.
- Cache ou leitura sob demanda por missão: a fatia não muda o modo como a App 09 carrega a
  trilha.
- Tocar a aferição, o corte de 60% ou a exceção da sondagem no núcleo — já corretos.

## Decisions

**1. O desafio é aninhado em `MissaoDoMestreSaida`, não em rota própria.**
A rota já é exclusiva do autor, já aninha o desafio de coleta pelo mesmo motivo, e a App 09 já
monta a bancada inteira a partir dela — o resumo da linha da missão passa a estar correto sem
uma segunda chamada por missão. _Descartada:_ `GET /v1/missoes/{id}/desbloqueio`, que pagaria
uma ida por missão aberta e deixaria o resumo da linha errado.

**2. A montagem reaproveita o que a declaração já usa.**
As perguntas saem de `perguntas_do_desbloqueio`, e a saída ao autor é a mesma
`PerguntaDoDesbloqueioAoAutorSaida` da declaração. Nada de forma nova para o mesmo dado — a
resposta da declaração e a da leitura precisam ser intercambiáveis, porque a App 09 alimenta o
mesmo formulário com as duas. _Descartada:_ uma saída reduzida na leitura, que faria o
formulário nascer diferente conforme a origem.

**3. As perguntas de todas as missões da trilha são lidas em uma consulta por trilha.**
`perguntas_do_desbloqueio` por missão, dentro do laço das missões, multiplicaria as consultas
pelo número de missões de cada trilha do Mestre. A leitura agrupa por missão da trilha e
distribui. O filtro de vigência (`substituida_em` nula) e a ordem são os mesmos da função que
já existe, para não haver duas noções de "pergunta vigente".

**4. A App 09 reaproveita o componente de imagem da App 05, não o compartilha.**
Copiar as ~30 linhas de `ImagemDaPergunta` para a App 09 custa menos que promover o componente
a `comum/`: ele depende do cliente de API de cada aplicação, e o projeto ainda não tem
precedente de componente comum que carregue bytes autenticados. Se um terceiro consumidor
aparecer, aí sim se promove. _Descartada:_ `<img src>` direto — toda rota sob `/v1` exige a
chave da aplicação em cabeçalho, que `<img>` não manda (decisão 6 da fatia 19).

**5. A sondagem muda o texto da tela, nunca o caminho do dado.**
`e_sondagem` já vem na missão. A tela deriva rótulo, abertura, aviso, resumo e a supressão da
escolha de tipo a partir dele; nenhuma rota, nenhum campo e nenhuma regra do núcleo muda. Na
sondagem o tipo declarado é sempre `quiz`, como `RF-09-81` fixa. _Descartada:_ um componente
`Sondagem` próprio na App 09 — duplicaria a montagem do quiz inteiro para trocar cinco frases.

**6. O comentário que documenta a ausência sai junto do conserto.**
`api.ts` afirma hoje que o desafio "nunca sai de `GET /trilhas/minhas`". Deixá-lo no lugar
faria o código descrever o defeito como se fosse projeto, e é assim que a fatia 18 chegou
até aqui.

## Risks / Trade-offs

- **A resposta de `/trilhas/minhas` cresce com o número de perguntas de todas as missões de
  todas as trilhas do Mestre** → o teto prático do Ciclo 01 é baixo, e o alternativo — uma
  ida por missão — troca peso por latência num público em rede fraca. Se crescer além do
  aceitável, a saída é paginar a bancada, não esconder o desafio de novo.
- **A alternativa correta passa a trafegar em mais uma resposta** → a rota já é do Mestre
  autor e já exige a credencial da persona; o cenário de recusa entra nos testes da rota, para
  que uma mudança futura em `MissaoSaida` não a exponha por descuido.
- **Copiar o componente de imagem cria duas cópias a manter** → aceito por ora; a promoção a
  `comum/` fica para o terceiro consumidor.
- **A sondagem some da escolha de tipo e alguém pode ter declarado prático nela antes** →
  `RF-09-81` nunca admitiu a sondagem prática, e nenhuma foi declarada em produção; a tela
  passa a montar o quiz direto.

## Open Questions

Nenhuma que trave a implementação. A pendência da sondagem publicada **sem nenhuma pergunta**
(`RF-09-82` confere só a existência da missão) fica registrada no documento 09 §1 para o
fundador decidir, e não é desta change.

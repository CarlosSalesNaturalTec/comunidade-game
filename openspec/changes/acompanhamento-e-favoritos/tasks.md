## 1. A entidade e a migração

- [ ] 1.1 Criar `backend/src/nucleo/favoritos/` (`__init__.py`, `modelo.py`, `regra.py`,
      `rotas.py`) e, em `modelo.py`, a entidade `Favorito` — `apoiador_id`, `guerreiro_id`,
      `mestre_id`, `incluido_em` —, com `CheckConstraint` de exatamente um alvo preenchido e
      duas `UniqueConstraint` parciais, uma por alvo (PRD-14 §8, design — decisão 3).
- [ ] 1.2 Escrever a migração Alembic aditiva de `favorito`, com o check e os dois índices
      únicos parciais; conferir que `alembic upgrade head` e o `downgrade` correspondente rodam
      limpos sobre o banco de teste (design — Migration Plan).

## 2. A regra do favorito

- [ ] 2.1 Em `regra.py`, `favoritar()`: alvo Guerreiro(a) resolvido por
      `vitrine.publico.buscar_persona_guerreiro_publica_por_nick` — nick exato, nick
      inexistente e nick sem autorização caindo no **mesmo** `NaoEncontrado`, sem desvio no
      código —, e alvo Mestre resolvido pela persona, com 404 para persona de outro papel. O
      alvo já favoritado devolve o favorito existente, com o mesmo corpo (`RF-14-49`,
      `RF-14-51`, `RF-14-52`, `RN-14-23`, design — decisões 4 e 5).
- [ ] 2.2 Em `regra.py`, `remover_favorito()` apagando a linha por `(id, apoiador_id)` em uma
      consulta só — favorito inexistente e favorito de outro Apoiador no mesmo 404 —, e
      `listar_favoritos()` trazendo Guerreiro(a) por avatar e nick sob
      `consentimentos.regra.condicao_de_autorizacao_vigente` dentro da consulta, e Mestre por
      nome e avatar (`RF-14-48`, `RF-14-52`, `RF-14-55`, `RN-14-24`, design — decisões 5 e 7).
- [ ] 2.3 Em `regra.py`, `montar_novidades()` derivando, por alvo e com janela de 30 dias a
      contar da data do fato, os quatro fatos disponíveis — criação original validada (com o
      mesmo portão de `listar_criacoes_publicas`, inclusive pela equipe), badge certificado,
      nível certificado e trilha publicada pelo Mestre —, em uma consulta por tipo de fato,
      sobre o conjunto de alvos (`RF-14-53`, `RN-14-25`, design — decisão 6).

## 3. As rotas

- [ ] 3.1 Em `rotas.py`, expor `GET`, `POST` e `DELETE` em `/v1/eu/favoritos`, restritas ao
      Apoiador em sessão e sempre sobre os favoritos de quem está em sessão, com
      `exigir_freio_por_origem("consulta_por_nick")` no `POST`; registrar o roteador em
      `backend/src/nucleo/principal.py` com `incluir_roteador_de_dados` (`RF-14-49`,
      `RF-14-52`, `RF-14-55`, PRD-14 §9, design — decisões 1, 2 e 8).
- [ ] 3.2 Cobrir a criação e a remoção em `backend/tests/test_favoritos.py`: nick exato de quem
      autorizou vira favorito; nick inexistente e nick sem autorização devolvem 404 idêntico,
      corpo por corpo; nick aproximado não alcança ninguém; nenhuma rota aceita fragmento de
      nick; Mestre favoritado por persona e persona de outro papel recusada; favoritar duas
      vezes não duplica e devolve o mesmo corpo; remoção some da lista; favorito de outro
      Apoiador e favorito inexistente no mesmo 404; papel diferente de Apoiador recusado com
      403 nas três rotas (`RF-14-49` a `RF-14-52`, `RF-14-55`, `RN-14-23`).
- [ ] 3.3 Cobrir a leitura em `backend/tests/test_favoritos.py`: os quatro fatos aparecem com a
      data, o de mais de 30 dias sai do destaque sem apagar nada, a trilha de outro Mestre não
      entra, a criação de equipe com integrante sem autorização não aparece; a revogação tira o
      favoritado da resposta sem lacuna nem contagem, e a autorização de volta o traz de volta;
      a saída de Guerreiro(a) é só avatar e nick, e a de Mestre não leva contato (`RF-14-48`,
      `RF-14-53`, `RF-14-54`, `RN-14-24`, `RN-14-25`).

## 4. A área de acompanhamento na App 08

- [ ] 4.1 Criar `apps/app-08-apoiador/src/acompanhamento/api.ts` com o cliente das três rotas
      de favorito e das rotas públicas de vitrine que a tela consome — estas **sem token de
      sessão** —, no padrão dos demais `api.ts` da aplicação (`RF-14-48`, design — decisão 9).
- [ ] 4.2 Criar `apps/app-08-apoiador/src/acompanhamento/TelaDeAcompanhamento.tsx` com o bloco
      do painel público, alimentado só pelas rotas públicas e sem recorte adicional
      (`RF-14-48`).
- [ ] 4.3 No mesmo arquivo, o bloco dos favoritos: campo de nick exato declarando que o nick
      vem da família, sem lista, sugestão ou autocompletar; a mesma mensagem para as duas
      recusas; a lista com Guerreiro(a) por avatar e nick e Mestre por nome e avatar; as
      novidades com a data; a declaração dos 30 dias e de que o destaque só existe nesta
      aplicação; a remoção; e o estado de quem ainda não favoritou ninguém (`RF-14-49` a
      `RF-14-55`, `RN-14-23`, `RN-14-25`, `RN-14-27`).
- [ ] 4.4 Ligar a área "Acompanhamento" na navegação de `apps/app-08-apoiador/src/App.tsx`, no
      padrão das demais áreas (`RF-14-48`, design — decisão 10).
- [ ] 4.5 Cobrir a área em `apps/app-08-apoiador/src/acompanhamento/acompanhamento.test.tsx`: o
      painel traz o que a vitrine traz e a chamada pública vai sem token; o campo é de nick
      exato e explica de onde vem o nick; as duas recusas mostram a mesma mensagem; favoritos
      aparecem com novidade e data; a tela declara os 30 dias e o alcance do destaque; sem
      favorito ela orienta; remover some da lista; e nenhuma tela oferece campo de mensagem ou
      contato (`RF-14-48` a `RF-14-55`).

## 5. Documentação

- [ ] 5.1 Marcar a fatia 7 do PRD-14 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug
      `acompanhamento-e-favoritos`, anotando na mesma linha que o quinto fato da novidade — o
      resultado de batalha — e a página pública do Mestre chegam com o PRD-10 e o PRD-03, e
      repetindo as duas pendências nos blocos daqueles PRDs. Nenhuma decisão de produto nova
      foi tomada: `docs/`, `docs/prds/index.md`, o documento 99 e a `nav` do `mkdocs.yml`
      seguem como estão.

## 1. Núcleo — o perfil declarado e o formato do comprovante

- [x] 1.1 Em `backend/src/nucleo/fila/modelo.py`, declarar o `StrEnum` `PerfilDeApoiador`
      (`pessoa_fisica`, `pessoa_juridica`) e a coluna `perfil`, nula, em
      `SolicitacaoDeParticipacao` — nula porque só a pretensão de Apoiador a declara
      (`RF-14-01`, `RN-14-39`)
- [x] 1.2 Escrever a migração Alembic que acrescenta a coluna `perfil`, com `downgrade` que a
      remove; verificar com `alembic upgrade head` seguido de `alembic downgrade -1`
      (`RF-14-01`)
- [x] 1.3 Em `fila/regra.py`, gravar o perfil recebido sem verificá-lo, recusar com 422 o perfil
      declarado em pretensão de Mestre e conferir o **formato do comprovante** — PDF, JPG ou
      PNG —, recusando com 422 e a lista dos formatos válidos, no molde do que `aportes` e
      `ressarcimentos` já aplicam (`RF-14-01`, `RF-14-04`, `RN-14-06`, `RN-14-39`)
- [x] 1.4 Em `fila/rotas.py`, aceitar `perfil` no formulário de
      `POST /v1/solicitacoes-de-participacao` e devolvê-lo em `SolicitacaoDeParticipacaoSaida`,
      que a gestão lê; o conteúdo do comprovante continua sem sair daqui (`RF-14-01`,
      `RN-14-39`, PRD-14 §11)

## 2. Testes do núcleo

- [x] 2.1 Em `backend/tests/test_fila.py`, cobrir a regra: perfil gravado como veio nas duas
      declarações, perfil em pretensão de Mestre recusado, comprovante em formato fora da lista
      recusado com os formatos válidos e nada gravado, e a permanência do que já valia — nick
      reservado, documento pessoal recusado e nenhuma persona criada (`RF-14-01`, `RF-14-04`,
      `RN-14-01`, `RN-14-03`, `RN-14-06`, `RN-14-39`)
- [x] 2.2 Em `backend/tests/test_fila_rota.py`, cobrir a rota pública: envio com perfil e
      comprovante devolvendo 201 sem abrir acesso, formato não aceito devolvendo 422 com os
      formatos, e o perfil aparecendo na leitura que o Admin faz da fila (`RF-14-01`,
      `RF-14-04`, `RF-14-05`, `RN-14-01`)

## 3. App 08 — a porta pública

- [x] 3.1 Em `apps/app-08-apoiador/src/api/configuracao.ts` e `.env.example`, acrescentar
      `VITE_URL_DO_FORMULARIO_DA_VITRINE`, vazia no Ciclo 01 (`RF-14-07`)
- [x] 3.2 Em `src/App.tsx`, apresentar a **porta pública** como tela padrão de quem não tem
      sessão, com o caminho para a entrada de quem já tem cadastro; nenhuma tela do Apoiador
      abre sem sessão (`RF-14-01`, `RF-01-02`, `RN-01-32`)
- [x] 3.3 Criar `src/preCadastro/api.ts` com o envio multipart de
      `POST /v1/solicitacoes-de-participacao` — sem token de sessão — e a leitura de
      `GET /v1/vitrine/necessidades`, ambos por `chamarNucleo` (`RF-14-02`, `RF-14-04`)
- [x] 3.4 Criar `src/preCadastro/escada.ts` com a escala fixa de 1 moeda = R$ 10,00 e as duas
      escadas do perfil (documento 04 §2), e a conversão que a tela usa para exibir o
      equivalente em moedas de qualquer valor, com fração de duas casas (`RF-14-03`,
      `RN-14-40`)
- [x] 3.5 Implementar `src/preCadastro/TelaDePreCadastro.tsx`: identificação sem documento —
      nome ou razão social, e-mail, WhatsApp, nick e perfil declarado —, as três formas de
      declarar o aporte (necessidade publicada, degrau da escada do perfil e valor livre), cada
      uma com o equivalente em moedas, e o anexo obrigatório do comprovante com os formatos
      declarados na tela (`RF-14-01` a `RF-14-04`, `RN-14-03`, `RN-14-39`, `RN-14-40`)
- [x] 3.6 Apresentar, antes do envio, que o pré-cadastro **não cria cadastro nem acesso**, que
      um Admin confere o comprovante e que a plataforma não emite recibo; enviado, confirmar
      que o pedido entrou na fila e continuar sem sessão (`RF-14-05`, `RN-14-01`)
- [x] 3.7 Apresentar a recusa do freio por origem com o tempo de espera em linguagem simples,
      preservando o que foi preenchido, e a recusa de formato com os formatos válidos
      (`RF-14-04`, `RF-14-06`)
- [x] 3.8 Encaminhar ao formulário da vitrine quem apoia com material, serviço ou divulgação,
      sem registrar aporte; sem endereço configurado, explicar o caminho em texto, sem link
      (`RF-14-07`, `RN-14-05`)

## 4. Testes da App 08

- [x] 4.1 Em `apps/app-08-apoiador/src/preCadastro/preCadastro.test.tsx`, cobrir a porta:
      quem não tem sessão vê a porta e a entrada, a tela não oferece campo de documento, a
      escada troca com o perfil declarado — a de pessoa física começando em 1 moeda —, o valor
      livre abaixo do menor degrau é aceito com o equivalente em moedas, o envio sem
      comprovante é recusado dizendo os formatos e a declaração de que nada ali cria acesso
      aparece antes do envio — critérios de aceite do PRD-14 §12 (`RF-14-01` a `RF-14-05`,
      `RN-14-03`, `RN-14-39`, `RN-14-40`)
- [x] 4.2 No mesmo arquivo, cobrir os desfechos: envio bem-sucedido confirmando a fila sem abrir
      sessão, 429 do freio mostrando o tempo de espera sem CAPTCHA e sem perder o preenchido,
      422 de formato mostrando os formatos válidos, e o encaminhamento à vitrine — com link
      quando há endereço e só texto quando não há (`RF-14-05` a `RF-14-07`, `RN-14-01`,
      `RN-14-05`)

## 5. Documentação

- [x] 5.1 Marcar a fatia 2 do PRD-14 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug da change e
      anotando na linha da fatia 5 que a opção "missão aberta" do `RF-14-02` entra com ela
- [x] 5.2 Acrescentar o **perfil declarado** à linha da `SolicitacaoDeParticipacao` no PRD-01
      §8, decisão do fundador de 2026-09-01. Nada mais muda em `docs/`: a fatia aplica o PRD-14
      como está, `docs/prds/index.md` só muda quando o PRD inteiro estiver implementado, e
      nenhum arquivo novo entra em `docs/` nem na `nav`

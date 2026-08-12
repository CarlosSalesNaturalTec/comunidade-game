## 1. Modelo de dados e migração

- [ ] 1.1 Criar o modelo `VinculoResponsavel` com os atributos do PRD-01 §8 — responsável,
      Guerreiro(a), grau de parentesco, cadastrado por, início e fim (`RF-01-13`, `RN-01-19`).
- [ ] 1.2 Criar o modelo `Consentimento` com os atributos do PRD-01 §8 — responsável,
      Guerreiro(a), tipo, versão do termo, decisão, data e hora, testemunha, anexo, origem e quem
      operou —, com `tipo` aberto e o anexo guardando referência, não binário (`RF-01-19`,
      `RN-01-12`, design — decisões).
- [ ] 1.3 Escrever a terceira migração Alembic criando as duas tabelas, sem tocar as das fatias
      anteriores, e conferir que ela sobe e desce.
- [ ] 1.4 Criar na mesma migração o _trigger_ que recusa `UPDATE` e `DELETE` em `consentimento`
      (`RN-01-12`, PRD-01 §8, design — decisões).

## 2. Cadastro do responsável e vínculo

- [ ] 2.1 Implementar `POST /v1/responsaveis`, restrita a Admin e Mestre pela operação
      `cadastro_de_responsavel` da matriz, criando a persona sem lhe dar acesso a Guerreiro(a)
      algum (`RF-01-13`, `RF-01-16`).
- [ ] 2.2 Implementar `POST /v1/responsaveis/{id}/vinculos`, restrita a Admin e Mestre pela
      operação `vinculo_com_guerreiros_e_guerreiras`, gravando quem cadastrou e o início
      (`RF-01-13`, `RF-01-16`).
- [ ] 2.3 Exigir o grau de parentesco em texto livre em cada vínculo, com 422 pelo corpo de erro
      único quando faltar (`RF-01-13`, `RN-01-19`).
- [ ] 2.4 Recusar vínculo com Guerreiro(a) que não está cadastrado, sem criar persona alguma
      (`RN-01-20`).
- [ ] 2.5 Implementar o teto de três responsáveis vigentes com `SELECT ... FOR UPDATE` na linha
      da persona do Guerreiro(a) antes de contar e inserir, respondendo 422 ao quarto
      (`RF-01-14`, `RN-01-19`, design — decisões).
- [ ] 2.6 Contar apenas vínculos vigentes no teto, de modo que vínculo encerrado não ocupe vaga
      (`RN-01-19`, documento 02 §1, design — decisões).

## 3. Recorte de leitura do responsável

- [ ] 3.1 Implementar a dependência `exigir_vinculo_do_responsavel`, que exige vínculo vigente
      quando o papel em sessão é responsável e nega por padrão (`RF-01-15`, `RF-01-16`).
- [ ] 3.2 Garantir que o recorte é o vínculo e não a comunidade: responsável não alcança criança
      da mesma comunidade sem vínculo com ela (`RF-01-15`).

## 4. Consentimento

- [ ] 4.1 Implementar `registrar_consentimento` como função de domínio, sem rota, concentrando as
      invariantes (`RF-01-19`, design — decisões).
- [ ] 4.2 Exigir a versão do termo, com 422 indicando o campo em falta quando faltar
      (`RN-01-12`).
- [ ] 4.3 Recusar consentimento sobre Guerreiro(a) não vinculado ao responsável que decide
      (`RF-01-15`, `RN-01-12`).
- [ ] 4.4 Implementar a revogação como inserção de registro novo, mantendo o anterior
      consultável, e o _listener_ de mapeador que recusa alteração e remoção (`RN-01-12`).
- [ ] 4.5 Implementar a consulta do que valia em uma data, respondendo pelo registro vigente
      naquela data (`RN-01-12`).
- [ ] 4.6 Garantir que nenhuma operação de participação é recusada por causa de consentimento
      recusado ou revogado (`RN-01-21`).

## 5. Verificação contra os critérios de aceite do PRD-01 §12

- [ ] 5.1 Teste: vincular um quarto responsável ao mesmo Guerreiro(a) é recusado com 422, e os
      três vínculos existentes continuam válidos, cada um com o seu grau de parentesco
      (`RF-01-14`, `RN-01-19`, PRD-01 §12).
- [ ] 5.2 Teste: o teto conta responsáveis de uma criança, não crianças de um responsável — o
      mesmo responsável se vincula a vários Guerreiros e Guerreiras (`RN-01-19`).
- [ ] 5.3 Teste concorrente: duas criações simultâneas do quarto vínculo não passam as duas
      (`RN-01-19`, design — decisões).
- [ ] 5.4 Teste: Guerreiro(a) com três vínculos, um encerrado, aceita um novo responsável
      (`RN-01-19`, documento 02 §1).
- [ ] 5.5 Teste: vínculo a Guerreiro(a) inexistente é recusado e nenhuma persona é criada
      (`RN-01-20`).
- [ ] 5.6 Teste: persona que não é Admin nem Mestre recebe 403 ao cadastrar responsável ou criar
      vínculo (`RF-01-13`, `RF-01-16`).
- [ ] 5.7 Teste: responsável recém-cadastrado, sem vínculo, não enxerga Guerreiro(a) algum, e o
      que tem vínculo enxerga só os seus (`RF-01-15`).
- [ ] 5.8 Teste: revogação de consentimento cria registro novo, e o anterior continua consultável
      (`RN-01-12`, PRD-01 §12).
- [ ] 5.9 Teste: `UPDATE` e `DELETE` em `consentimento` são recusados **também fora do ORM**,
      direto no banco (`RN-01-12`, design — decisões).
- [ ] 5.10 Teste: consentimento sem versão do termo é recusado com 422 e nada é gravado
      (`RN-01-12`).
- [ ] 5.11 Teste: recusa de consentimento não impede a participação do Guerreiro(a), e a
      revogação não desfaz o que ele já realizou (`RN-01-21`).
- [ ] 5.12 Teste: toda escrita nova desta fatia grava autor, papel e data e hora com fuso
      (`RF-01-03`, regressão da fatia anterior).
- [ ] 5.13 Teste: rota nova sem chave de aplicação responde 401, sem diferenciar o motivo
      (`RN-01-32`, regressão da fatia 1).
- [ ] 5.14 Rodar `ruff format --check .`, `ruff check .` e `pytest` na pasta `backend/`, as três
      verdes.

## 6. Documentação e esteira

- [ ] 6.1 Conferir que nenhuma decisão nova foi tomada nesta change e que, portanto, nenhum
      documento-fonte e o documento 09 mudam.
- [ ] 6.2 Conferir que nenhuma relação entre documentos mudou, que nenhum arquivo novo entrou em
      `docs/` e que `docs/prds/index.md` segue refletindo a situação.
- [ ] 6.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.

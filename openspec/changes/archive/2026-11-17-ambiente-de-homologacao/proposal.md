# Ambiente de homologação

**Origem:** infraestrutura transversal (sem PRD) — linha "Ambiente de homologação" do
`openspec/cronograma-de-fatias.md`, sem número de fatia. Aplica a decisão do fundador de
2026-11-17 no documento 03 §1, princípio 13, e na linha "Ambiente de homologação" do
documento 09 §1. Toca `RF-01-54` e `RN-01-51` (chave por aplicação e por ambiente) sem mudar
o enunciado deles: muda só a contagem de ambientes.

## Why

A plataforma está em produção, com aulas reais, e os testes também estão sendo lançados lá.
Lançamento de teste em produção vira histórico permanente — o livro-razão e os pontos só se
corrigem por estorno — e contamina ranking, vitrine e indicadores. Falta um lugar para testar.

## What Changes

- O núcleo passa a conhecer o ambiente **`homologacao`**, ao lado de `desenvolvimento` e
  `producao`. A conferência da chave, a semeadura e a guarda de arranque (bucket obrigatório)
  valem para ele como valem para produção.
- A semeadura passa a convergir **oito chaves por ambiente em três ambientes — 24 chaves**.
- **Homologação no Cloud Run**: serviço, Job de migração e conta de execução próprios, com a
  **mesma imagem** que vai a produção; **base própria na mesma instância `nucleo-db`**, bucket,
  segredos e sites do Firebase Hosting próprios.
- **Esteiras de deploy**: o merge em `main` passa a publicar **na homologação**, não mais em
  produção. Produção passa a receber a versão escolhida **só por disparo manual** de um
  workflow de produção, com o `sha` validado como entrada. **BREAKING** para a operação: o
  merge deixa de atualizar produção.
- Os sites de homologação não são indexados por buscadores.
- **Fora do escopo:** estorno ou limpeza dos lançamentos de teste já feitos em produção —
  ficam como estão (decisão do fundador); gerador de dados sintéticos — a homologação nasce
  vazia, com as chaves e o Admin fundador, e o dado de teste é criado pelas próprias
  aplicações; cópia de dado de produção para a homologação, que é vedada.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `chave-de-aplicacao`: a semeadura por ambiente passa de dois para três ambientes (24
  chaves), e a chave de homologação não abre produção nem o contrário.

## Impact

- `backend/src/nucleo/configuracao.py` (`Ambiente`, guarda de arranque), `chaves/` (semeadura
  e conferência, sem mudança de formato da chave `cg_<ambiente>_<id>.<segredo>`).
- `.github/workflows/backend-deploy.yml` e os sete `app-NN-deploy.yml`; workflow novo de
  promoção a produção.
- `firebase.json` e `.firebaserc` (alvos de homologação, inclusive o `api` com _rewrite_ para o
  serviço de homologação).
- Google Cloud, por provisionamento manual do fundador: base e usuário na `nucleo-db`, bucket,
  conta de execução, segredos, sites do Firebase e origens no cliente OAuth do Google.
- GitHub: _environments_ `homologacao` e `producao`, com os segredos de cada um.
- Custo: Cloud Run com mínimo zero, base na instância existente e sites no free tier — o
  acréscimo é o do bucket, lançado como recurso de _cloud_ no aporte por absorção já vigente.

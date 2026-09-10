# Bucket de armazenamento em produção

Origem: **PRD-09** (`RF-09-19`, envio retomável do conteúdo da missão), **PRD-07** (`RF-07-49`,
artefato comprobatório) e **PRD-04** (anexo do termo), entre as oito capacidades que dependem
da porta de armazenamento. Todas `implementado` no cronograma e **nenhuma no ar**.
Provisionamento, não fatia: linha sem número no bloco do PRD-09.

## Why

`CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE` nunca foi declarada em produção. O `backend/README.md`
diz que sem ela "o núcleo cai para disco local" — **o código não faz isso**. Em produção a
fábrica devolve sempre o adaptador de nuvem, e o construtor estoura com o nome vazio:

```text
IndexError: string index out of range   # google/cloud/storage/_helpers.py, _validate_name
```

`_validate_name` não tem guarda de comprimento antes de `name[0]`. Como a porta é resolvida por
requisição, o erro acontece antes de qualquer byte ser tocado: nenhum envio chegou a disco
efêmero, porque nenhum envio começou. Oito módulos respondem 500 desde o primeiro deploy —
`aportes`, `armazenamento`, `coletas`, `consentimentos`, `conteudos`, `criacoes_originais`,
`fila` e `ressarcimentos`.

Duas correções acompanham o provisionamento:

1. **A frase do README é falsa** e esconde o sintoma real de quem for diagnosticar.
2. **A falta se anuncia tarde e mal.** Configuração de produção ausente deveria impedir o
   arranque com uma frase que diz o que falta, não estourar `IndexError` numa requisição
   qualquer, horas depois, para um usuário.

## What Changes

- `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE` declarada em `--set-env-vars` do
  `backend-deploy.yml`, ao lado de `CG_AMBIENTE` e `CG_GEMINI_MODELO`: **nome de bucket não é
  segredo**, mesmo critério já aplicado ao modelo.
- Arranque falha cedo, com mensagem nomeando a variável, quando o ambiente é produção e o
  bucket não foi declarado. Vale para a porta de armazenamento; a porta de IA continua
  degradando com aviso, porque ali a indisponibilidade é requisito (`RF-09-91`).
- README: apagar a frase do fallback, documentar a criação do bucket e o papel que a
  `nucleo-runtime` precisa.
- Testes do adaptador de nuvem do armazenamento, que hoje não tem nenhum.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. As oito capacidades já especificam o envio e a leitura do arquivo; a change faz o
destino existir. `skip_specs: true`.

## Impact

| Área | O que muda |
| --- | --- |
| `.github/workflows/backend-deploy.yml` | a variável em `--set-env-vars`, nas duas etapas |
| `backend/src/nucleo/configuracao.py` ou `armazenamento/fabrica.py` | a falha cedo em produção |
| `backend/README.md` | frase do fallback, provisionamento do bucket e papel da conta |
| `backend/tests/` | cobertura do adaptador de nuvem e da falha cedo |
| `openspec/cronograma-de-fatias.md` | linha sem número no bloco do PRD-09 |

Fora do repositório, a cargo do fundador: criar o bucket em `southamerica-east1` e conceder à
`nucleo-runtime` acesso a objeto nele — ela tem hoje apenas `secretmanager.secretAccessor` e
`cloudsql.client`.

**Duas decisões do fundador ficam pendentes** e travam as tarefas: o **nome do bucket** e se
ele nasce com **versionamento e regra de ciclo de vida**. Não se resolvem aqui.

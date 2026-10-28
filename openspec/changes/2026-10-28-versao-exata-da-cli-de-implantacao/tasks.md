# Tasks

## 1. Versão e gatilho do `backend-deploy.yml`

- [ ] 1.1 No passo "Publicar o alvo `api` no Firebase Hosting", trocar
      `npx --yes firebase-tools@latest` por `npx --yes firebase-tools@15.28.1` e acrescentar
      acima da chamada o comentário que justifica a versão exata, no mesmo teor do que
      `app-09-deploy.yml` carrega — a CLI é baixada a cada publicação e sem fixá-la o
      comportamento do deploy muda sozinho entre duas execuções; subir a versão é ato
      revisado. Verificar que `grep -rn "firebase-tools" .github/workflows/ | grep -v
      "15.28.1"` não devolve nenhuma chamada, isto é, que as oito esteiras de publicação
      citam a mesma versão.
- [ ] 1.2 Nos `paths` do gatilho `push`, acrescentar `.github/workflows/backend-deploy.yml`
      aos dois itens que já estão lá, preservando `backend/**` e a exclusão
      `!backend/**.md` — sem incluir `firebase.json` nem `.firebaserc`, pelo motivo no
      `design.md`. Verificar que o YAML _parseia_
      (`python -c "import yaml; yaml.safe_load(open('.github/workflows/backend-deploy.yml'))"`)
      e que o `git diff` do arquivo mostra apenas a versão, o comentário e os `paths`.

## 2. A regra em lugar vivo

- [ ] 2.1 Em `CLAUDE.md`, na seção "As três esteiras", acrescentar um item à lista que segue
      a tabela, junto do que já trata do caminho que cada workflow cobre: a CLI de
      implantação vai em **versão exata**, nunca `@latest` nem faixa `^`, porque é baixada a
      cada publicação. Uma linha, sem repetir a justificativa que o workflow já carrega.
      Verificar que o item existe, que a numeração e a largura de linha da seção seguem como
      antes e que nenhuma outra seção do arquivo foi tocada.

## 3. Documentação

- [ ] 3.1 Acrescentar à tabela do documento 09 §1 duas linhas, no formato das demais — tema
      na primeira coluna, situação e encaminhamento na segunda, com o rastro desta change:
      (a) **permissão de Service Usage da conta de deploy**, que não tem
      `serviceusage.services.get` e por isso faz o gcloud registrar "Skipped validating" e
      fez a CLI nova abortar; é ato no console do Google Cloud, fora do repositório;
      (b) **republicação do rewrite do alvo `api`**, que não acontece quando o
      `firebase.json` muda, porque o gatilho do workflow não olha o arquivo — a saída é
      separar aquela publicação do deploy do núcleo. Verificar que as duas linhas estão na
      §1, que a tabela continua fechando e que nada mais no documento mudou.
- [ ] 3.2 Acrescentar a linha desta change à tabela **Infraestrutura transversal (sem PRD)**
      de `openspec/cronograma-de-fatias.md`, com `—` na coluna Fatia, o slug na coluna
      Recorte e `implementado` na Situação. Nada muda em `docs/prds/index.md`, no documento
      99 nem na `nav` do `mkdocs.yml`: a change não altera requisito de PRD, não cria
      arquivo em `docs/` e não muda relação entre documentos. Verificar que a linha está na
      tabela certa e que nenhum bloco de PRD foi tocado.

## Workflow follow-up

- Depois do merge em `main`, conferir que o `Backend Deploy` disparou pelos `paths` novos e
  que o passo do Firebase Hosting concluiu — é a prova da correção, e republica o rewrite
  que ficou sem publicar no merge do PR #272.

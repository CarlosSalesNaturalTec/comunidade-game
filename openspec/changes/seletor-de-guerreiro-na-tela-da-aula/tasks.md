# Tasks

## 1. Tela da aula

- [ ] 1.1 Em `TelaDaAula.tsx`, carregar todas as páginas de `listarGuerreirosVinculaveis`
      ao abrir a tela, com aviso em linguagem simples se falhar (`RF-09-45`, `RF-09-46`,
      `RN-09-18`)
- [ ] 1.2 Trocar o campo "Identificador do Guerreiro(a)" do formulário de presença por um
      seletor por nick, ordenado, sem quem já consta da lista de presentes (`RF-09-45`,
      `RN-09-18`)
- [ ] 1.3 Trocar o mesmo campo do formulário de ocorrência por um seletor por nick com todos
      os Guerreiros e Guerreiras (`RF-09-46`, `RN-09-18`)
- [ ] 1.4 Impedir o envio dos dois formulários sem Guerreiro(a) escolhido, com mensagem em
      linguagem simples (`RF-09-45`, `RF-09-46`)

## 2. Testes

- [ ] 2.1 Em `turmas.test.tsx`, ajustar os testes da tela da aula ao seletor e cobrir os
      cenários "O Mestre confirma a presença que faltou", "O Guerreiro(a) é escolhido pelo
      nick, nunca digitado", "Quem já está presente não é oferecido de novo" e "Enviar sem
      escolher o Guerreiro(a) é impedido" (`RF-09-45`, `RF-09-46`, `RN-09-18`)

## 3. Documentação

- [ ] 3.1 Acrescentar a linha "—" "Seletor de Guerreiro(a) na tela da aula" ao bloco do
      PRD-09 em `openspec/cronograma-de-fatias.md`, como implementada; nada em `docs/` muda —
      sem decisão nem requisito novo

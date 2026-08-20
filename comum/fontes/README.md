# Procedência das fontes

Os quatro `.woff2` deste diretório são cópias, não dependência de tempo de instalação
(design — Decisions). Atualizar a fonte é um gesto deliberado: repetir os passos abaixo com a
versão nova e revisar o resultado, nunca um `npm update`.

| Família                        | Arquivo                                     | Eixo variável                  | Subconjunto  |
| ------------------------------- | -------------------------------------------- | ------------------------------- | ------------ |
| Atkinson Hyperlegible Next v7   | `atkinson-hyperlegible-next-latin.woff2`     | peso `200–800`                  | latin        |
| Atkinson Hyperlegible Next v7   | `atkinson-hyperlegible-next-latin-ext.woff2` | peso `200–800`                  | latin-ext    |
| Archivo v25                     | `archivo-latin.woff2`                        | peso `100–900`, largura `62–125%` | latin        |
| Archivo v25                     | `archivo-latin-ext.woff2`                    | peso `100–900`, largura `62–125%` | latin-ext    |

- **Origem:** Google Fonts (`https://github.com/google/fonts`), pelos pacotes publicados
  `@fontsource-variable/atkinson-hyperlegible-next@5.3.0` e `@fontsource-variable/archivo@5.3.0`
  — usados só como fonte de extração dos `.woff2` já subconjuntados; nenhum dos dois entra como
  dependência do `package.json` (design — Decisions).
- **Data da cópia:** 2026-08-20.
- **Licença:** SIL Open Font License 1.1, uma por família — `OFL-atkinson-hyperlegible-next.txt`
  e `OFL-archivo.txt`, ao lado dos arquivos, como a licença exige.

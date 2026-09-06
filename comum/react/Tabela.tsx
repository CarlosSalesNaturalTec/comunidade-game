import type { ReactNode } from "react";

export interface ColunaDaTabela<T> {
  chave: string;
  rotulo: string;
  /** `th scope="row"` em vez de `td` — a célula que identifica a linha. */
  cabecalhoDeLinha?: boolean;
  /** Recolhida abaixo do marco de `768` px da §4; volta a partir dele
   * (design — decisão 1). */
  recolhida?: boolean;
  renderizar: (linha: T) => ReactNode;
}

interface Props<T> {
  legenda?: ReactNode;
  colunas: ColunaDaTabela<T>[];
  linhas: T[];
  chaveDaLinha: (linha: T) => string;
}

// Tabela semântica — `th` com escopo, legenda opcional em `caption` — com
// a rolagem horizontal confinada ao próprio componente, para a página
// nunca rolar de lado (documento 15 §6, design — decisão 2).
export function Tabela<T>({ legenda, colunas, linhas, chaveDaLinha }: Props<T>) {
  return (
    <div className="cg-tabela__rolagem">
      <table className="cg-tabela">
        {legenda && <caption>{legenda}</caption>}
        <thead>
          <tr>
            {colunas.map((coluna) => (
              <th
                key={coluna.chave}
                scope="col"
                className={coluna.recolhida ? "cg-tabela__coluna-recolhida" : undefined}
              >
                {coluna.rotulo}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {linhas.map((linha) => (
            <tr key={chaveDaLinha(linha)}>
              {colunas.map((coluna) => {
                const className = coluna.recolhida ? "cg-tabela__coluna-recolhida" : undefined;
                return coluna.cabecalhoDeLinha ? (
                  <th key={coluna.chave} scope="row" className={className}>
                    {coluna.renderizar(linha)}
                  </th>
                ) : (
                  <td key={coluna.chave} className={className}>
                    {coluna.renderizar(linha)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

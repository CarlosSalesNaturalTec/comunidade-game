import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type ChaveDeAplicacao, listarChaves } from "./api";
import { ListaDeChaves } from "./ListaDeChaves";

// Área ao lado das Filas, não dentro delas — a fila mostra pedidos, o
// painel mostra chaves já emitidas, com ciclo próprio (design — decisão 4,
// `RF-02-90`).
export function TelaDeChaves() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [chaves, definirChaves] = useState<ChaveDeAplicacao[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const ehAdmin = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao || !ehAdmin) return;
    try {
      const pagina = await listarChaves(sessao.token);
      definirChaves(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar as chaves. Tente novamente em instantes.");
    }
  }, [sessao, ehAdmin, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Chaves" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {!ehAdmin && (
        <Aviso tipo="atencao">
          Esta área é do Admin. Fale com um Admin da comunidade se precisar consultar as chaves
          emitidas.
        </Aviso>
      )}

      {ehAdmin && (
        <>
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
          <ListaDeChaves chaves={chaves} aoRevogar={carregar} />
        </>
      )}
    </Moldura>
  );
}

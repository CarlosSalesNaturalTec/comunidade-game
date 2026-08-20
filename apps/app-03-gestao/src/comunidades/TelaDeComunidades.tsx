import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { type ComunidadeDaLista, listarComunidades } from "./api";
import { FormularioDeComunidade } from "./FormularioDeComunidade";
import { ListaDeComunidades } from "./ListaDeComunidades";

export function TelaDeComunidades() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

  const carregar = useCallback(async () => {
    try {
      const pagina = await listarComunidades();
      definirComunidades(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar as comunidades. Tente novamente em instantes.");
    }
  }, [tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const aoCriar = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  // O caminho de criação não é oferecido a quem não é Admin (`RN-02-04`,
  // `RN-08-01`, PRD-02 §4).
  const podeCriar = sessao?.papel === "admin";

  return (
    <Moldura>
      <Cabecalho titulo="Comunidades Virtuais" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {podeCriar && !mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Nova comunidade</Botao>
      )}

      {podeCriar && mostrarFormulario && (
        <FormularioDeComunidade
          onCriada={aoCriar}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDeComunidades comunidades={comunidades} />
    </Moldura>
  );
}

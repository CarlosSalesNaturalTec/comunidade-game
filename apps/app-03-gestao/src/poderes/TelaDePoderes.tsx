import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { listarPoderes, type PoderDaLista } from "./api";
import { FormularioDePoder } from "./FormularioDePoder";
import { ListaDePoderes } from "./ListaDePoderes";

// Área ao lado de Comunidades, por ser cadastro de catálogo — bem comum da
// plataforma, e não dado de comunidade (design — decisões, `RF-02-10`).
export function TelaDePoderes() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [poderes, definirPoderes] = useState<PoderDaLista[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [poderEmEdicao, definirPoderEmEdicao] = useState<PoderDaLista | null>(null);

  // Toda persona em sessão lê o catálogo; só o Admin escreve (`RF-02-10`,
  // `RF-01-28`).
  const podeGerenciar = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const pagina = await listarPoderes(sessao.token);
      definirPoderes(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar os poderes. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const aoCriar = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  const aoConcluirEdicao = useCallback(async () => {
    definirPoderEmEdicao(null);
    await carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Poderes" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {podeGerenciar && !mostrarFormulario && !poderEmEdicao && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Novo poder</Botao>
      )}

      {podeGerenciar && mostrarFormulario && (
        <FormularioDePoder
          onSalvo={aoCriar}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      {podeGerenciar && poderEmEdicao && (
        <FormularioDePoder
          poder={poderEmEdicao}
          onSalvo={aoConcluirEdicao}
          onCancelar={() => definirPoderEmEdicao(null)}
        />
      )}

      <ListaDePoderes
        poderes={poderes}
        podeGerenciar={podeGerenciar}
        aoEditar={definirPoderEmEdicao}
        aoDesativar={carregar}
      />
    </Moldura>
  );
}

import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { listarPoderes, type PoderDoCatalogo } from "../poderes/api";
import { listarMinhasTrilhas, type TrilhaDoMestre } from "../trilhas/api";
import { FormularioDeTrilha } from "../trilhas/FormularioDeTrilha";
import { ListaDeTrilhas } from "../trilhas/ListaDeTrilhas";
import { TelaDaTrilha } from "../trilhas/TelaDaTrilha";

// A casa do Mestre: a lista das próprias trilhas, a criação de uma nova e,
// ao abrir uma, a autoria de missão, atividade e cadência de retomada
// (PRD-09 §6.1).
export function TelaDeAutoria() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [trilhas, definirTrilhas] = useState<TrilhaDoMestre[] | null>(null);
  const [poderes, definirPoderes] = useState<PoderDoCatalogo[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [idDaTrilhaAberta, definirIdDaTrilhaAberta] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [lista, paginaDePoderes] = await Promise.all([
        listarMinhasTrilhas(sessao.token),
        listarPoderes(sessao.token),
      ]);
      definirTrilhas(lista);
      definirPoderes(paginaDePoderes.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar as suas trilhas. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const trilhaAberta = trilhas?.find((trilha) => trilha.id === idDaTrilhaAberta) ?? null;

  function atualizarTrilhaLocal(trilhaAtualizada: TrilhaDoMestre) {
    definirTrilhas(
      (atual) =>
        atual?.map((trilha) =>
          trilha.id === trilhaAtualizada.id ? trilhaAtualizada : trilha,
        ) ?? atual,
    );
  }

  if (trilhaAberta) {
    return (
      <TelaDaTrilha
        trilha={trilhaAberta}
        aoVoltar={() => definirIdDaTrilhaAberta(null)}
        onAtualizarTrilha={atualizarTrilhaLocal}
      />
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Minhas trilhas" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {!mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Nova trilha</Botao>
      )}

      {mostrarFormulario && (
        <FormularioDeTrilha
          poderes={poderes}
          onSalvo={async () => {
            definirMostrarFormulario(false);
            await carregar();
          }}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDeTrilhas
        trilhas={trilhas}
        poderes={poderes}
        aoAbrir={(trilha) => definirIdDaTrilhaAberta(trilha.id)}
      />
    </Moldura>
  );
}

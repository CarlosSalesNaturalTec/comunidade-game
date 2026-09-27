import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { listarResponsaveis, type ResponsavelDaLista } from "./api";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { ListaDeResponsaveis } from "./ListaDeResponsaveis";

const DADO_COLETADO = "o nome do responsável e o vínculo dele com os Guerreiros e Guerreiras";

// A sub-área tinha só o botão de cadastrar: responsável cadastrado ficava
// inalcançável pela gestão, e o cadastro interrompido antes do vínculo não
// aparecia em lugar nenhum. A lista o revela, e a linha retoma o vínculo pela
// rota que já existe — nenhum cadastro novo (`RF-02-111`, design — decisão 7).
export function TelaDeResponsaveis() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [responsaveis, definirResponsaveis] = useState<ResponsavelDaLista[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [cadastrando, definirCadastrando] = useState(false);
  const [emRetomada, definirEmRetomada] = useState<ResponsavelDaLista | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const pagina = await listarResponsaveis(sessao.token);
      definirResponsaveis(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar os responsáveis. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const aoConcluir = useCallback(async () => {
    definirCadastrando(false);
    definirEmRetomada(null);
    definirResponsaveis(null);
    await carregar();
  }, [carregar]);

  if (cadastrando || emRetomada !== null) {
    return (
      <FormularioDeResponsavel
        responsavelExistente={emRetomada}
        onConcluido={aoConcluir}
        onCancelar={aoConcluir}
      />
    );
  }

  return (
    <div>
      <AvisoDeColeta dado={DADO_COLETADO} />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={() => definirCadastrando(true)}>Cadastrar responsável</Botao>
      <ListaDeResponsaveis responsaveis={responsaveis} onRetomar={definirEmRetomada} />
    </div>
  );
}

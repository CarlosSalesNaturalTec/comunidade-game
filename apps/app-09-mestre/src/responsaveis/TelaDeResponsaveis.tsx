import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { listarResponsaveis, type ResponsavelDaLista } from "./api";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { ListaDeResponsaveis } from "./ListaDeResponsaveis";

const DADO_COLETADO = "o nome do responsável e o vínculo dele com os Guerreiros e Guerreiras";

// A área abria direto no cadastro, e responsável cadastrado ficava
// inalcançável — pior no Mestre, que cadastra presencialmente e é quem mais
// interrompe o cadastro antes do vínculo. Passa a abrir na lista que o núcleo
// já recorta para ele, com o cadastro atrás de um botão e a retomada do
// vínculo na linha (`RF-09-122`, design — decisões 1 e 3).
//
// O recorte não se repete aqui: quem decide o que o Mestre alcança é
// `GET /v1/responsaveis` (design — decisão 5).
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

  return (
    <Moldura>
      <Cabecalho
        titulo="Responsáveis"
        subtitulo="Os responsáveis das suas comunidades e os que você cadastrou."
      />
      {cadastrando || emRetomada !== null ? (
        <FormularioDeResponsavel responsavelExistente={emRetomada} onConcluido={aoConcluir} />
      ) : (
        <div>
          <AvisoDeColeta dado={DADO_COLETADO} />
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
          <Botao onClick={() => definirCadastrando(true)}>Cadastrar responsável</Botao>
          <ListaDeResponsaveis responsaveis={responsaveis} onRetomar={definirEmRetomada} />
        </div>
      )}
    </Moldura>
  );
}

import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useId, useState } from "react";
import type { AdultoDaLista } from "../personas/api";
import { designarResponsavel } from "./api";

interface Props {
  idDoPontoDeApoio: string;
  adultos: AdultoDaLista[];
  onDesignado: () => void;
}

const MENSAGEM_DE_FALHA =
  "Não foi possível designar o responsável. Tente novamente em instantes.";

// Oferecido só ao Admin, entre os Mestres e Apoiadores cadastrados — o
// núcleo também aceita Admin, mas sem `GET /v1/admins` a tela não inventa
// lista (`RF-02-52`, `RF-07-49`, `RN-07-34`; design — decisão 4).
export function DesignarResponsavel({ idDoPontoDeApoio, adultos, onDesignado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoSeletor = useId();
  const [aberto, definirAberto] = useState(false);
  const [responsavelId, definirResponsavelId] = useState(adultos[0]?.id ?? "");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Designar responsável
      </Botao>
    );
  }

  async function confirmar() {
    if (!responsavelId || !sessao) return;

    definirErro(null);
    definirEnviando(true);
    try {
      await designarResponsavel(idDoPontoDeApoio, responsavelId, sessao.token);
      definirAberto(false);
      onDesignado();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro(MENSAGEM_DE_FALHA);
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="designar-responsavel">
      <label htmlFor={idDoSeletor}>Responsável pelo acervo</label>
      <select
        id={idDoSeletor}
        value={responsavelId}
        onChange={(evento) => definirResponsavelId(evento.target.value)}
      >
        {adultos.map((adulto) => (
          <option key={adulto.id} value={adulto.id}>
            {adulto.nome}
          </option>
        ))}
      </select>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar
      </Botao>
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Cancelar
      </Botao>
    </div>
  );
}

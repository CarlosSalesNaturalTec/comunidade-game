import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { gravarContorno } from "./api";

interface Props {
  idDaComunidade: string;
  nomeDaComunidade: string;
  substituindo: boolean;
  onGravado: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: "geometria" | "origem_osm";
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin grava o contorno da comunidade.";

// O que se copia do OSM costuma vir como `Feature` ou `FeatureCollection`, e o
// núcleo aceita só a geometria: tira-se o invólucro, sem mexer no dado. O que
// não for nenhum dos dois segue como veio, e o núcleo decide (design —
// Decisão 2).
export function geometriaDoTextoColado(objeto: unknown): unknown {
  if (typeof objeto !== "object" || objeto === null) return objeto;
  const registro = objeto as Record<string, unknown>;
  if (registro.type === "Feature" && "geometry" in registro) {
    return registro.geometry;
  }
  if (
    registro.type === "FeatureCollection" &&
    Array.isArray(registro.features) &&
    registro.features.length === 1
  ) {
    const feicao = registro.features[0] as Record<string, unknown> | null;
    if (feicao && typeof feicao === "object" && "geometry" in feicao) {
      return feicao.geometry;
    }
  }
  return objeto;
}

// Cadastro e substituição do contorno pelo Admin. A tela só confere vazio e
// JSON malformado; tipo, anel, faixa de coordenada e padrão da origem são do
// núcleo (`RF-02-122`, `RF-08-33`).
export function FormularioDeContorno({
  idDaComunidade,
  nomeDaComunidade,
  substituindo,
  onGravado,
  onCancelar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTexto = useId();
  const [texto, definirTexto] = useState("");
  const [origem, definirOrigem] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!texto.trim()) {
      definirErroDeCampo({ campo: "geometria", mensagem: "Cole o GeoJSON do contorno." });
      return;
    }
    let objeto: unknown;
    try {
      objeto = JSON.parse(texto);
    } catch {
      definirErroDeCampo({
        campo: "geometria",
        mensagem: "O texto colado não é um GeoJSON válido.",
      });
      return;
    }
    if (!origem.trim()) {
      definirErroDeCampo({
        campo: "origem_osm",
        mensagem: "Informe o elemento de origem no OSM, como relation/12582832.",
      });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      await gravarContorno(
        idDaComunidade,
        { geometria: geometriaDoTextoColado(objeto), origem_osm: origem.trim() },
        sessao.token,
      );
      onGravado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      if (
        erro instanceof ErroDaApi &&
        erro.codigo === "erro_de_validacao" &&
        (erro.campo === "geometria" || erro.campo === "origem_osm")
      ) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa("Não foi possível gravar o contorno. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  const erroDaGeometria = erroDeCampo?.campo === "geometria" ? erroDeCampo.mensagem : null;

  return (
    <form onSubmit={aoSubmeter} aria-label={`Contorno de ${nomeDaComunidade}`}>
      <div className="cg-campo">
        <label htmlFor={idDoTexto}>GeoJSON do contorno</label>
        <textarea
          id={idDoTexto}
          value={texto}
          onChange={(evento) => definirTexto(evento.target.value)}
          aria-invalid={erroDaGeometria ? true : undefined}
          aria-describedby={erroDaGeometria ? `${idDoTexto}-erro` : undefined}
        />
        {erroDaGeometria && (
          <p id={`${idDoTexto}-erro`} role="alert" className="cg-campo__erro">
            {erroDaGeometria}
          </p>
        )}
      </div>

      <Campo
        rotulo="Elemento de origem no OSM"
        valor={origem}
        aoAlterar={definirOrigem}
        erro={erroDeCampo?.campo === "origem_osm" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        {substituindo ? "Substituir" : "Cadastrar"}
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}

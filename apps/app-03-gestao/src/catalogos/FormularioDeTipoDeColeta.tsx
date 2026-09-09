import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  cadastrarTipoDeColeta,
  type FormaDeRegistro,
  ROTULO_DA_FORMA_DE_REGISTRO,
} from "./api";

interface Props {
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin cadastra tipo de coleta do catálogo.";

// Unidade e faixa esperada só existem no tipo que se mede por número — é o
// `CheckConstraint` que o núcleo já impõe, trazido para antes do envio; a
// recusa do núcleo segue sendo apresentada quando vier (`RF-02-108`,
// `RF-08-12`, `RF-08-21`, design — decisão 5).
export function FormularioDeTipoDeColeta({ onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaForma = useId();
  const [nome, definirNome] = useState("");
  const [formaDeRegistro, definirFormaDeRegistro] = useState<FormaDeRegistro>("numero");
  const [unidade, definirUnidade] = useState("");
  const [faixaMinima, definirFaixaMinima] = useState("");
  const [faixaMaxima, definirFaixaMaxima] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const medePorNumero = formaDeRegistro === "numero";

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do tipo de coleta." });
      return;
    }
    if (medePorNumero) {
      if (!unidade.trim()) {
        definirErroDeCampo({
          campo: "unidade",
          mensagem: "O tipo que se mede por número exige unidade.",
        });
        return;
      }
      if (!faixaMinima.trim() || !faixaMaxima.trim()) {
        definirErroDeCampo({
          campo: "faixa",
          mensagem:
            "O tipo que se mede por número exige a faixa esperada, com mínimo e máximo.",
        });
        return;
      }
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      await cadastrarTipoDeColeta(
        medePorNumero
          ? {
              nome,
              forma_de_registro: formaDeRegistro,
              unidade,
              faixa_minima: Number(faixaMinima),
              faixa_maxima: Number(faixaMaxima),
            }
          : { nome, forma_de_registro: formaDeRegistro },
        sessao.token,
      );
      onSalvo();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      // A faixa invertida volta do núcleo apontando `faixa_minima`; a
      // mensagem aparece no campo da faixa (`RF-08-12`).
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        const campo =
          erro.campo === "faixa_minima" || erro.campo === "faixa_maxima"
            ? "faixa"
            : erro.campo;
        definirErroDeCampo({ campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível cadastrar o tipo de coleta. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo tipo de coleta">
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaForma}>Forma de registro</label>
        <select
          id={idDaForma}
          value={formaDeRegistro}
          onChange={(evento) => definirFormaDeRegistro(evento.target.value as FormaDeRegistro)}
          aria-invalid={erroDeCampo?.campo === "forma_de_registro" || undefined}
        >
          {Object.entries(ROTULO_DA_FORMA_DE_REGISTRO).map(([valor, rotulo]) => (
            <option key={valor} value={valor}>
              {rotulo}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "forma_de_registro" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {medePorNumero ? (
        <>
          <Campo
            rotulo="Unidade"
            valor={unidade}
            aoAlterar={definirUnidade}
            erro={erroDeCampo?.campo === "unidade" ? erroDeCampo.mensagem : null}
          />

          <Campo
            rotulo="Faixa esperada — mínimo"
            tipo="number"
            valor={faixaMinima}
            aoAlterar={definirFaixaMinima}
          />

          <Campo
            rotulo="Faixa esperada — máximo"
            tipo="number"
            valor={faixaMaxima}
            aoAlterar={definirFaixaMaxima}
            erro={erroDeCampo?.campo === "faixa" ? erroDeCampo.mensagem : null}
          />
        </>
      ) : (
        <Aviso tipo="atencao">
          O tipo que se mede por foto ou vídeo não pede unidade nem faixa esperada: a mídia é o
          próprio registro.
        </Aviso>
      )}

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Cadastrar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}

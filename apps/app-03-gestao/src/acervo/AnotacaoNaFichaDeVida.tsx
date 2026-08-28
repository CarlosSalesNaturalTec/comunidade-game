import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { anotarFichaDeVida, type TeorDaAnotacao } from "./api";

interface Props {
  idDoItem: string;
  onAnotado: () => void;
}

const TEORES: { valor: TeorDaAnotacao; rotulo: string }[] = [
  { valor: "cuidado", rotulo: "Cuidado" },
  { valor: "perda", rotulo: "Perda" },
  { valor: "dano", rotulo: "Dano" },
];

const RECUSA_POR_PAPEL = "Só Admin ou Mestre anotam a ficha de vida.";
const MENSAGEM_DE_FALHA =
  "Não foi possível registrar a anotação. Tente novamente em instantes.";

// Oferecida a Admin e Mestre. Perda e dano se anotam, e nunca viram débito
// ao Guerreiro(a) nem à família — a tela não pede nem oferece campo para
// identificar culpado (`RF-02-55`, `RN-02-14`, `RN-02-15`, `RN-02-16`,
// documento 05 §3.6).
export function AnotacaoNaFichaDeVida({ idDoItem, onAnotado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTeor = useId();
  const [aberto, definirAberto] = useState(false);
  const [teor, definirTeor] = useState<TeorDaAnotacao>("cuidado");
  const [estadoDeConservacao, definirEstadoDeConservacao] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Anotar
      </Botao>
    );
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!estadoDeConservacao.trim()) {
      definirErroDeCampo("Informe o estado de conservação apurado.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await anotarFichaDeVida(
        idDoItem,
        { teor, estado_de_conservacao: estadoDeConservacao },
        sessao.token,
      );
      definirAberto(false);
      definirEstadoDeConservacao("");
      definirTeor("cuidado");
      onAnotado();
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
        erro.campo === "estado_de_conservacao"
      ) {
        definirErroDeCampo(erro.message);
        return;
      }
      definirErroDeRecusa(MENSAGEM_DE_FALHA);
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Anotar na ficha de vida">
      <div className="cg-campo">
        <label htmlFor={idDoTeor}>Teor</label>
        <select
          id={idDoTeor}
          value={teor}
          onChange={(evento) => definirTeor(evento.target.value as TeorDaAnotacao)}
        >
          {TEORES.map((item) => (
            <option key={item.valor} value={item.valor}>
              {item.rotulo}
            </option>
          ))}
        </select>
      </div>

      {(teor === "perda" || teor === "dano") && (
        <Aviso tipo="atencao">
          Nada é debitado ao Guerreiro(a) nem à família por esta anotação.
        </Aviso>
      )}

      <Campo
        rotulo="Estado de conservação apurado"
        valor={estadoDeConservacao}
        aoAlterar={definirEstadoDeConservacao}
        erro={erroDeCampo}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Confirmar anotação
      </Botao>
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Cancelar
      </Botao>
    </form>
  );
}

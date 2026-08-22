import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import type { PoderDoCatalogo } from "../poderes/api";
import { criarTrilha } from "./api";

interface Props {
  poderes: PoderDoCatalogo[];
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

// O Mestre não escreve trilha sem um poder do catálogo — nome, objetivo e
// área do conhecimento são exigidos aqui mesmo, sem chamar o núcleo, porque
// `criar_trilha` não valida esses três (design — decisões; `RF-09-01`).
export function FormularioDeTrilha({ poderes, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoPoder = useId();
  const idDoErroDoPoder = `${idDoPoder}-erro`;
  const [nome, definirNome] = useState("");
  const [objetivo, definirObjetivo] = useState("");
  const [areaDoConhecimento, definirAreaDoConhecimento] = useState("");
  const [poderId, definirPoderId] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  // O seletor oferece só poder ativo e de natureza de Guerreiro(a) — o
  // Poder Sustentador nunca aparece aqui (`RF-09-01`, `RN-01-43`).
  const poderesDeGuerreiro = poderes.filter(
    (poder) => poder.ativo && poder.natureza === "de_guerreiro",
  );

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome da trilha." });
      return;
    }
    if (!objetivo.trim()) {
      definirErroDeCampo({ campo: "objetivo", mensagem: "Informe o objetivo da trilha." });
      return;
    }
    if (!areaDoConhecimento.trim()) {
      definirErroDeCampo({
        campo: "area_do_conhecimento",
        mensagem: "Informe a área do conhecimento.",
      });
      return;
    }
    if (!poderId) {
      definirErroDeCampo({ campo: "poder_id", mensagem: "Escolha um poder do catálogo." });
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      await criarTrilha(
        { nome, objetivo, area_do_conhecimento: areaDoConhecimento, poder_id: poderId },
        sessao.token,
      );
      onSalvo();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa("Não foi possível criar a trilha. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Nova trilha">
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Objetivo"
        valor={objetivo}
        aoAlterar={definirObjetivo}
        erro={erroDeCampo?.campo === "objetivo" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Área do conhecimento"
        valor={areaDoConhecimento}
        aoAlterar={definirAreaDoConhecimento}
        erro={erroDeCampo?.campo === "area_do_conhecimento" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoPoder}>Poder</label>
        <select
          id={idDoPoder}
          value={poderId}
          onChange={(evento) => definirPoderId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "poder_id" || undefined}
          aria-describedby={erroDeCampo?.campo === "poder_id" ? idDoErroDoPoder : undefined}
        >
          <option value="">Selecione um poder</option>
          {poderesDeGuerreiro.map((poder) => (
            <option key={poder.id} value={poder.id}>
              {poder.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "poder_id" && (
          <p id={idDoErroDoPoder} role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Criar trilha
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}

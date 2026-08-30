import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  alterarPoder,
  cadastrarPoder,
  type NaturezaDoPoder,
  type PapelDoPoder,
  type PoderDaLista,
  type VigenciaDoPoder,
} from "./api";

interface Props {
  poder?: PoderDaLista;
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin cadastra, altera ou desativa poder do catálogo.";

const ROTULO_DA_NATUREZA: Record<NaturezaDoPoder, string> = {
  de_guerreiro: "De guerreiro",
  derivado_do_aporte: "Derivado do aporte",
};

const ROTULO_DA_VIGENCIA: Record<VigenciaDoPoder, string> = {
  vigente: "Vigente",
  ciclo_futuro: "Ciclo futuro",
};

const ROTULO_DO_PAPEL: Record<PapelDoPoder, string> = {
  territorio: "Papel do Território",
};

// Cadastro e edição no mesmo formulário: a natureza e o papel só entram no
// cadastro, porque `alterar_poder` não os admite — mudar a natureza
// reescreveria o vínculo já concedido às trilhas (`RF-02-10`, `RN-01-43`,
// `RN-01-54`).
export function FormularioDePoder({ poder, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const emEdicao = poder !== undefined;
  const idDaNatureza = useId();
  const idDaVigencia = useId();
  const idDoPapel = useId();
  const idDoTecnico = useId();
  const [nome, definirNome] = useState(poder?.nome ?? "");
  const [descricao, definirDescricao] = useState(poder?.descricao ?? "");
  const [natureza, definirNatureza] = useState<NaturezaDoPoder>(
    poder?.natureza ?? "de_guerreiro",
  );
  const [vigencia, definirVigencia] = useState<VigenciaDoPoder>(poder?.vigencia ?? "vigente");
  const [papel, definirPapel] = useState<PapelDoPoder | "">(poder?.papel ?? "");
  const [tecnico, definirTecnico] = useState(poder?.tecnico ?? false);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    // Campo obrigatório em falta é apontado no campo, sem chamar o núcleo
    // e sem gravar nada (`RF-02-10`).
    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do poder." });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      if (emEdicao) {
        await alterarPoder(poder.id, { nome, descricao, vigencia, tecnico }, sessao.token);
      } else {
        await cadastrarPoder(
          { nome, descricao, natureza, vigencia, papel: papel || undefined, tecnico },
          sessao.token,
        );
      }
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
      // O segundo poder com o papel do Território é recusado com 409, e a
      // mensagem do núcleo já é clara o bastante para aparecer como está
      // (`RN-01-54`).
      if (
        erro instanceof ErroDaApi &&
        erro.codigo === "papel_do_poder_territorio_ja_declarado"
      ) {
        definirErroDeRecusa(erro.message);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        emEdicao
          ? "Não foi possível alterar o poder. Tente novamente em instantes."
          : "Não foi possível cadastrar o poder. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label={emEdicao ? "Editar Poder" : "Novo Poder"}>
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />

      <Campo rotulo="Descrição" valor={descricao} aoAlterar={definirDescricao} />

      {emEdicao ? (
        <Aviso tipo="atencao">
          A natureza ({ROTULO_DA_NATUREZA[natureza]}) não muda depois de cadastrada.
          {poder?.papel &&
            ` O papel (${ROTULO_DO_PAPEL[poder.papel]}) também não muda por aqui.`}
        </Aviso>
      ) : (
        <>
          <div className="cg-campo">
            <label htmlFor={idDaNatureza}>Natureza</label>
            <select
              id={idDaNatureza}
              value={natureza}
              onChange={(evento) => definirNatureza(evento.target.value as NaturezaDoPoder)}
            >
              {Object.entries(ROTULO_DA_NATUREZA).map(([valor, rotulo]) => (
                <option key={valor} value={valor}>
                  {rotulo}
                </option>
              ))}
            </select>
          </div>

          <Aviso tipo="atencao">A natureza não muda depois de cadastrada.</Aviso>

          <div className="cg-campo">
            <label htmlFor={idDoPapel}>Papel</label>
            <select
              id={idDoPapel}
              value={papel}
              onChange={(evento) => definirPapel(evento.target.value as PapelDoPoder | "")}
            >
              <option value="">Nenhum</option>
              {Object.entries(ROTULO_DO_PAPEL).map(([valor, rotulo]) => (
                <option key={valor} value={valor}>
                  {rotulo}
                </option>
              ))}
            </select>
          </div>
        </>
      )}

      <div className="cg-campo">
        <label htmlFor={idDaVigencia}>Vigência</label>
        <select
          id={idDaVigencia}
          value={vigencia}
          onChange={(evento) => definirVigencia(evento.target.value as VigenciaDoPoder)}
        >
          {Object.entries(ROTULO_DA_VIGENCIA).map(([valor, rotulo]) => (
            <option key={valor} value={valor}>
              {rotulo}
            </option>
          ))}
        </select>
      </div>

      <div className="cg-campo">
        <label htmlFor={idDoTecnico}>
          <input
            id={idDoTecnico}
            type="checkbox"
            checked={tecnico}
            onChange={(evento) => definirTecnico(evento.target.checked)}
          />{" "}
          Este é um poder técnico
        </label>
        <p>
          Marque para que o template de missão sugira, nas trilhas deste poder, uma atividade
          desplugada — sem tela nem eletrônico.
        </p>
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        {emEdicao ? "Salvar" : "Cadastrar"}
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}

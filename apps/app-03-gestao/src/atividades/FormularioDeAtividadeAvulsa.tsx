import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { listarPoderes, type PoderDaLista } from "../poderes/api";
import {
  type AtividadeAvulsa,
  cadastrarAtividadeAvulsa,
  type FormatoDeAtividade,
  type ModalidadeDeAtividade,
} from "./api";

interface Props {
  onCadastrada: (atividade: AtividadeAvulsa) => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const MODALIDADES: { valor: ModalidadeDeAtividade; rotulo: string }[] = [
  { valor: "individual", rotulo: "Individual" },
  { valor: "em_equipe", rotulo: "Em equipe" },
  { valor: "em_equipe_com_familiar", rotulo: "Em equipe com familiar" },
];

const FORMATOS: { valor: FormatoDeAtividade; rotulo: string }[] = [
  { valor: "presencial", rotulo: "Presencial" },
  { valor: "on_line_assincrona", rotulo: "On-line assíncrona" },
];

const RECUSA_POR_PAPEL = "Só o Admin cadastra a atividade avulsa.";

// Sem campo de pontuação — o motor deriva pelo desfecho lançado — e sem
// campo de recurso — quem declara é a aula (`RF-02-29`, documento 11 §5).
export function FormularioDeAtividadeAvulsa({ onCadastrada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaModalidade = useId();
  const idDoFormato = useId();
  const idDoPoder = useId();

  const [poderes, definirPoderes] = useState<PoderDaLista[]>([]);
  const [titulo, definirTitulo] = useState("");
  const [descricao, definirDescricao] = useState("");
  const [modalidade, definirModalidade] = useState<ModalidadeDeAtividade>("individual");
  const [formato, definirFormato] = useState<FormatoDeAtividade>("presencial");
  const [natureza, definirNatureza] = useState("");
  const [producaoEsperada, definirProducaoEsperada] = useState("");
  const [poderId, definirPoderId] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarPoderes(sessao.token).then((pagina) => definirPoderes(pagina.itens));
  }, [sessao]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!titulo.trim()) {
      definirErroDeCampo({ campo: "titulo", mensagem: "Informe o título." });
      return;
    }
    if (!natureza.trim()) {
      definirErroDeCampo({ campo: "natureza", mensagem: "Informe a natureza." });
      return;
    }
    if (!producaoEsperada.trim()) {
      definirErroDeCampo({
        campo: "producao_esperada",
        mensagem: "Informe o que o Guerreiro(a) produz.",
      });
      return;
    }
    if (!poderId) {
      definirErroDeCampo({
        campo: "poder_id",
        mensagem: "Escolha o poder que ela desenvolve.",
      });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const atividade = await cadastrarAtividadeAvulsa(
        {
          titulo,
          descricao: descricao.trim() || undefined,
          modalidade,
          formato,
          natureza,
          producao_esperada: producaoEsperada,
          poder_id: poderId,
        },
        sessao.token,
      );
      onCadastrada(atividade);
      definirTitulo("");
      definirDescricao("");
      definirNatureza("");
      definirProducaoEsperada("");
      definirPoderId("");
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível cadastrar a atividade. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Cadastrar atividade avulsa">
      <Campo
        rotulo="Título"
        valor={titulo}
        aoAlterar={definirTitulo}
        erro={erroDeCampo?.campo === "titulo" ? erroDeCampo.mensagem : null}
      />
      <Campo rotulo="Descrição" valor={descricao} aoAlterar={definirDescricao} />

      <div className="cg-campo">
        <label htmlFor={idDaModalidade}>Modalidade</label>
        <select
          id={idDaModalidade}
          value={modalidade}
          onChange={(evento) =>
            definirModalidade(evento.target.value as ModalidadeDeAtividade)
          }
        >
          {MODALIDADES.map((item) => (
            <option key={item.valor} value={item.valor}>
              {item.rotulo}
            </option>
          ))}
        </select>
      </div>

      <div className="cg-campo">
        <label htmlFor={idDoFormato}>Formato</label>
        <select
          id={idDoFormato}
          value={formato}
          onChange={(evento) => definirFormato(evento.target.value as FormatoDeAtividade)}
        >
          {FORMATOS.map((item) => (
            <option key={item.valor} value={item.valor}>
              {item.rotulo}
            </option>
          ))}
        </select>
      </div>

      <Campo
        rotulo="Natureza"
        valor={natureza}
        aoAlterar={definirNatureza}
        erro={erroDeCampo?.campo === "natureza" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Produção esperada"
        valor={producaoEsperada}
        aoAlterar={definirProducaoEsperada}
        erro={erroDeCampo?.campo === "producao_esperada" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoPoder}>Poder que ela desenvolve</label>
        <select
          id={idDoPoder}
          value={poderId}
          onChange={(evento) => definirPoderId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "poder_id" || undefined}
        >
          <option value="">Escolha um poder</option>
          {poderes.map((poder) => (
            <option key={poder.id} value={poder.id}>
              {poder.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "poder_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Cadastrar atividade
      </Botao>
    </form>
  );
}

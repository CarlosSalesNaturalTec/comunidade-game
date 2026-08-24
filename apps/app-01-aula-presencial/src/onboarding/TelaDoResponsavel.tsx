import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useRef, useState } from "react";
import { cadastrarResponsavelNoEncontro, criarVinculo } from "../api/responsaveis";

interface Props {
  tokenDeTrabalho: string;
  guerreiroId: string;
  aoConcluir: (responsavelId: string) => void;
  aoVoltar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

// O responsável mínimo do encontro: nome e grau de parentesco, sem e-mail,
// senha nem documento — atos da gestão, fora desta tela (`RF-04-60`, PRD-04
// §§3.2, 5.2). Se o vínculo falhar depois do responsável já criado, a
// retentativa não recria o responsável — só o vínculo (design — decisão 4).
export function TelaDoResponsavel({
  tokenDeTrabalho,
  guerreiroId,
  aoConcluir,
  aoVoltar,
}: Props) {
  const [nome, definirNome] = useState("");
  const [grauDeParentesco, definirGrauDeParentesco] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const responsavelIdCriado = useRef<string | null>(null);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do responsável." });
      return;
    }
    if (!grauDeParentesco.trim()) {
      definirErroDeCampo({
        campo: "grau_de_parentesco",
        mensagem: "Informe o grau de parentesco.",
      });
      return;
    }

    definirEnviando(true);
    try {
      if (!responsavelIdCriado.current) {
        const responsavel = await cadastrarResponsavelNoEncontro(
          { nome: nome.trim() },
          tokenDeTrabalho,
        );
        responsavelIdCriado.current = responsavel.id;
      }
      await criarVinculo(
        responsavelIdCriado.current,
        { guerreiro_id: guerreiroId, grau_de_parentesco: grauDeParentesco.trim() },
        tokenDeTrabalho,
      );
      aoConcluir(responsavelIdCriado.current);
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi && erroCapturado.campo) {
        definirErroDeCampo({ campo: erroCapturado.campo, mensagem: erroCapturado.message });
        return;
      }
      definirErroDeCampo({
        campo: "geral",
        mensagem: "Não foi possível cadastrar o responsável. Tente novamente.",
      });
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Responsável presente"
        subtitulo="Nome e grau de parentesco — o acesso da família é resolvido pela gestão."
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />
      <form onSubmit={aoSubmeter} aria-label="Cadastro do responsável">
        <Campo
          rotulo="Nome do responsável"
          valor={nome}
          aoAlterar={definirNome}
          erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
        />
        <Campo
          rotulo="Grau de parentesco"
          valor={grauDeParentesco}
          aoAlterar={definirGrauDeParentesco}
          erro={erroDeCampo?.campo === "grau_de_parentesco" ? erroDeCampo.mensagem : null}
        />
        {erroDeCampo?.campo === "geral" && <Aviso tipo="erro">{erroDeCampo.mensagem}</Aviso>}
        <Botao tipo="submit" desabilitado={enviando}>
          {enviando ? "Cadastrando…" : "Continuar para o termo"}
        </Botao>
      </form>
    </Moldura>
  );
}

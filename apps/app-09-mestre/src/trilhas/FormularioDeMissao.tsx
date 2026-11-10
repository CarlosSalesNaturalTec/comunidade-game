import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  type CorrecaoDaMissao,
  corrigirMissao,
  criarMissao,
  type EtapaDoCiclo,
  type MissaoDaTrilha,
} from "./api";

// Com `missao`, o formulário corrige o que está gravado em vez de criar: os
// campos chegam preenchidos e a posição some, porque ela muda só pela ordem
// (`RF-09-136`, design — decisão 8).
interface Props {
  idDaTrilha: string;
  proximaPosicao: number;
  etapaInicial: EtapaDoCiclo;
  onSalvo: (missao: MissaoDaTrilha) => void;
  onCancelar: () => void;
  missao?: MissaoDaTrilha;
  trilhaPublicada?: boolean;
  onCorrigida?: (correcao: CorrecaoDaMissao) => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const ROTULO_DA_ETAPA: Record<EtapaDoCiclo, string> = {
  abertura: "Abertura",
  desenvolvimento: "Desenvolvimento",
  marcos: "Marcos",
  fechamento: "Fechamento",
};

// A obrigatoriedade nunca nasce com um valor padrão — o Mestre declara,
// como `RF-09-80` exige (design — decisões).
export function FormularioDeMissao({
  idDaTrilha,
  proximaPosicao,
  etapaInicial,
  onSalvo,
  onCancelar,
  missao,
  trilhaPublicada = false,
  onCorrigida,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaObrigatoriedade = useId();
  const idDaEtapa = useId();
  const idDaSondagem = useId();
  const [titulo, definirTitulo] = useState(missao?.titulo ?? "");
  const [posicao, definirPosicao] = useState(String(proximaPosicao));
  const [nivelDeDificuldade, definirNivelDeDificuldade] = useState(
    String(missao?.nivel_de_dificuldade ?? 1),
  );
  const [obrigatoria, definirObrigatoria] = useState<"" | "sim" | "nao">(
    missao ? (missao.obrigatoria ? "sim" : "nao") : "",
  );
  const [etapaDoCiclo, definirEtapaDoCiclo] = useState<EtapaDoCiclo>(
    missao?.etapa_do_ciclo ?? etapaInicial,
  );
  const [eSondagem, definirESondagem] = useState(missao?.e_sondagem ?? false);
  const [materiais, definirMateriais] = useState<string[]>(missao?.materiais ?? []);
  const [novoMaterial, definirNovoMaterial] = useState("");
  const [confirmandoDespublicacao, definirConfirmandoDespublicacao] = useState(false);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  // Item em branco nunca entra na lista (`RF-09-140`).
  function acrescentarMaterial() {
    const nome = novoMaterial.trim();
    if (!nome) return;
    definirMateriais((atuais) => [...atuais, nome]);
    definirNovoMaterial("");
  }

  function removerMaterial(indice: number) {
    definirMateriais((atuais) => atuais.filter((_, posicao) => posicao !== indice));
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!titulo.trim()) {
      definirErroDeCampo({ campo: "titulo", mensagem: "Informe o título da missão." });
      return;
    }
    if (!obrigatoria) {
      definirErroDeCampo({
        campo: "obrigatoria",
        mensagem: "Declare se a missão é obrigatória ou opcional.",
      });
      return;
    }

    // Desmarcar a sondagem de trilha publicada a tira do ar: a tela diz isso
    // antes de gravar, e só grava com a confirmação (`RF-09-139`, `RN-09-59`).
    const despublica = Boolean(missao && trilhaPublicada && missao.e_sondagem && !eSondagem);
    if (despublica && !confirmandoDespublicacao) {
      definirConfirmandoDespublicacao(true);
      return;
    }
    definirConfirmandoDespublicacao(false);

    if (!sessao) return;
    definirEnviando(true);
    try {
      if (missao) {
        const correcao = await corrigirMissao(
          missao.id,
          {
            titulo,
            nivel_de_dificuldade: Number(nivelDeDificuldade),
            obrigatoria: obrigatoria === "sim",
            etapa_do_ciclo: etapaDoCiclo,
            e_sondagem: eSondagem,
            // Só manda a lista quando ela mudou, para não reescrever o que
            // não foi tocado (design — decisão 6).
            ...(materiaisMudaram(missao.materiais ?? [], materiais) ? { materiais } : {}),
          },
          sessao.token,
        );
        onCorrigida?.(correcao);
        return;
      }
      const criada = await criarMissao(
        idDaTrilha,
        {
          titulo,
          posicao: Number(posicao),
          nivel_de_dificuldade: Number(nivelDeDificuldade),
          obrigatoria: obrigatoria === "sim",
          etapa_do_ciclo: etapaDoCiclo,
          e_sondagem: eSondagem,
          materiais,
        },
        sessao.token,
      );
      onSalvo(criada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      const CAMPOS_COM_LUGAR_NA_TELA = new Set(["titulo", "obrigatoria", "e_sondagem"]);
      if (
        erro instanceof ErroDaApi &&
        erro.campo &&
        CAMPOS_COM_LUGAR_NA_TELA.has(erro.campo)
      ) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      // Toda recusa do núcleo chega traduzida — mesmo quando o campo dela
      // não tem um lugar próprio nesta tela, a mensagem (já em linguagem
      // simples) aparece no aviso geral, nunca some (`RF-09-12`).
      if (erro instanceof ErroDaApi) {
        definirErroDeRecusa(erro.message);
        return;
      }
      definirErroDeRecusa(
        missao
          ? "Não foi possível corrigir a missão. Tente novamente em instantes."
          : "Não foi possível acrescentar a missão. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form
      onSubmit={aoSubmeter}
      aria-label={missao ? `Corrigir a missão ${missao.titulo}` : "Nova missão"}
    >
      <Campo
        rotulo="Título"
        valor={titulo}
        aoAlterar={definirTitulo}
        erro={erroDeCampo?.campo === "titulo" ? erroDeCampo.mensagem : null}
      />
      {!missao && (
        <Campo rotulo="Posição" tipo="number" valor={posicao} aoAlterar={definirPosicao} />
      )}
      <Campo
        rotulo="Nível de dificuldade"
        tipo="number"
        valor={nivelDeDificuldade}
        aoAlterar={definirNivelDeDificuldade}
      />

      <div className="cg-campo">
        <label htmlFor={idDaObrigatoriedade}>Obrigatoriedade</label>
        <select
          id={idDaObrigatoriedade}
          value={obrigatoria}
          onChange={(evento) => definirObrigatoria(evento.target.value as "" | "sim" | "nao")}
          aria-invalid={erroDeCampo?.campo === "obrigatoria" || undefined}
        >
          <option value="">Selecione</option>
          <option value="sim">Obrigatória</option>
          <option value="nao">Opcional</option>
        </select>
        {erroDeCampo?.campo === "obrigatoria" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <div className="cg-campo">
        <label htmlFor={idDaEtapa}>Etapa do ciclo</label>
        <select
          id={idDaEtapa}
          value={etapaDoCiclo}
          onChange={(evento) => definirEtapaDoCiclo(evento.target.value as EtapaDoCiclo)}
        >
          {Object.entries(ROTULO_DA_ETAPA).map(([valor, rotulo]) => (
            <option key={valor} value={valor}>
              {rotulo}
            </option>
          ))}
        </select>
      </div>

      <div className="cg-campo">
        <label htmlFor={idDaSondagem}>
          <input
            id={idDaSondagem}
            type="checkbox"
            checked={eSondagem}
            onChange={(evento) => definirESondagem(evento.target.checked)}
          />{" "}
          Esta é a missão de sondagem que abre a trilha
        </label>
        {erroDeCampo?.campo === "e_sondagem" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <fieldset className="cg-campo">
        <legend>Materiais necessários para a aula</legend>
        <p>Opcional. Por exemplo: cola, jumpers, papel.</p>
        {materiais.length > 0 && (
          <ul aria-label="Materiais declarados">
            {materiais.map((material, indice) => (
              // biome-ignore lint/suspicious/noArrayIndexKey: nomes podem se repetir
              <li key={`${indice}-${material}`}>
                {material}{" "}
                <Botao variante="secundaria" onClick={() => removerMaterial(indice)}>
                  Remover {material}
                </Botao>
              </li>
            ))}
          </ul>
        )}
        <Campo rotulo="Novo material" valor={novoMaterial} aoAlterar={definirNovoMaterial} />
        <Botao variante="secundaria" onClick={acrescentarMaterial}>
          Acrescentar material
        </Botao>
      </fieldset>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      {confirmandoDespublicacao && (
        <p role="alert">
          Esta trilha está publicada. Sem a missão de sondagem, ela sai do ar ao gravar, e para
          publicar de novo vai faltar a sondagem. Confirme para gravar assim mesmo.
        </p>
      )}

      <Botao tipo="submit" desabilitado={enviando}>
        {confirmandoDespublicacao
          ? "Confirmar e tirar a trilha do ar"
          : missao
            ? "Gravar correção"
            : "Acrescentar missão"}
      </Botao>
      <Botao
        variante="secundaria"
        onClick={
          confirmandoDespublicacao ? () => definirConfirmandoDespublicacao(false) : onCancelar
        }
      >
        {confirmandoDespublicacao ? "Voltar sem gravar" : "Cancelar"}
      </Botao>
    </form>
  );
}

function materiaisMudaram(gravados: string[], atuais: string[]): boolean {
  return gravados.length !== atuais.length || gravados.some((nome, i) => nome !== atuais[i]);
}

import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import type { AdultoDaLista, ArtefatoComprobatorio } from "./api";
import { cadastrarApoiador, cadastrarMestre } from "./api";
import { FormularioDeArtefatos } from "./FormularioDeArtefatos";

interface ValorInicial {
  nome?: string;
  email?: string;
  whatsapp?: string;
  nick?: string;
}

interface Props {
  papel: "mestre" | "apoiador";
  onSalvo: (adulto: AdultoDaLista) => void;
  onCancelar: () => void;
  // Pré-preenchimento a partir da solicitação de participação aceita
  // (`RF-02-20`); editável, e o cadastro continua exigindo as mesmas
  // coisas de sempre — aceitar, por si só, não cadastra ninguém
  // (`RN-02-03`).
  valorInicial?: ValorInicial;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const ROTULO_DO_PAPEL: Record<Props["papel"], string> = {
  mestre: "Mestre",
  apoiador: "Apoiador",
};

export function FormularioDeAdulto({ papel, onSalvo, onCancelar, valorInicial }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [nome, definirNome] = useState(valorInicial?.nome ?? "");
  const [email, definirEmail] = useState(valorInicial?.email ?? "");
  const [whatsapp, definirWhatsapp] = useState(valorInicial?.whatsapp ?? "");
  const [nick, definirNick] = useState(valorInicial?.nick ?? "");
  const [artefatos, definirArtefatos] = useState<ArtefatoComprobatorio[]>([]);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome." });
      return;
    }
    if (!email.trim()) {
      definirErroDeCampo({ campo: "email", mensagem: "Informe o e-mail." });
      return;
    }
    // A confirmação nunca avança sem ao menos um artefato (`RF-02-04`).
    const artefatosPreenchidos = artefatos.filter(
      (artefato) => artefato.endereco.trim() && artefato.rotulo.trim(),
    );
    if (artefatosPreenchidos.length === 0) {
      definirErroDeCampo({
        campo: "artefatos",
        mensagem: "Ao menos um artefato comprobatório é obrigatório.",
      });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      const cadastrar = papel === "mestre" ? cadastrarMestre : cadastrarApoiador;
      const adulto = await cadastrar(
        {
          nome,
          email,
          whatsapp: whatsapp || undefined,
          nick: nick || undefined,
          artefatos: artefatosPreenchidos,
        },
        sessao.token,
      );
      onSalvo(adulto);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(`Só o Admin cadastra ${ROTULO_DO_PAPEL[papel]}.`);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa("Não foi possível cadastrar. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label={`Novo ${ROTULO_DO_PAPEL[papel]}`}>
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="E-mail"
        tipo="email"
        valor={email}
        aoAlterar={definirEmail}
        erro={erroDeCampo?.campo === "email" ? erroDeCampo.mensagem : null}
      />
      <Campo rotulo="WhatsApp (opcional)" valor={whatsapp} aoAlterar={definirWhatsapp} />
      {valorInicial?.nick !== undefined && (
        <Campo rotulo="Nick pretendido" valor={nick} aoAlterar={definirNick} />
      )}

      <FormularioDeArtefatos
        artefatos={artefatos}
        aoAlterar={definirArtefatos}
        erro={erroDeCampo?.campo === "artefatos" ? erroDeCampo.mensagem : null}
      />

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

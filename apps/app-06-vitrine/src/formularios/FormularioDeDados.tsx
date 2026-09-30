import { Aviso, Botao, Moldura } from "comum/react";
import { useState } from "react";
import { enviarSolicitacaoDeDados } from "../api/solicitacoes";
import { navegarPara } from "../navegacao/navegar";
import { CampoDeTexto } from "./CampoDeTexto";
import { useEnvio } from "./useEnvio";

const FORMATADOR = new Intl.DateTimeFormat("pt-BR", { dateStyle: "long" });
const OBRIGATORIOS = "Preencha este campo.";

interface Props {
  irPara?: (destino: string) => void;
}

/** Solicitação do conjunto de dados (`RF-03-32` a `RF-03-34`, PRD-03 §5.2).
 * O recorte pedido é exigido pelo núcleo (design — decisão 3). */
export function FormularioDeDados({ irPara = navegarPara }: Props) {
  const [solicitante, definirSolicitante] = useState("");
  const [instituicao, definirInstituicao] = useState("");
  const [email, definirEmail] = useState("");
  const [finalidade, definirFinalidade] = useState("");
  const [recorte, definirRecorte] = useState("");
  const [faltando, definirFaltando] = useState<Record<string, boolean>>({});

  const { estado, disparar } = useEnvio(() =>
    enviarSolicitacaoDeDados({
      solicitante: solicitante.trim(),
      instituicao: instituicao.trim(),
      email: email.trim(),
      finalidade_declarada: finalidade.trim(),
      recorte_pedido: recorte.trim(),
    }),
  );

  function aoEnviar(evento: React.FormEvent) {
    evento.preventDefault();
    const ausentes = {
      solicitante: !solicitante.trim(),
      instituicao: !instituicao.trim(),
      email: !email.trim(),
      finalidade: !finalidade.trim(),
      recorte: !recorte.trim(),
    };
    definirFaltando(ausentes);
    if (Object.values(ausentes).some(Boolean)) return;
    void disparar();
  }

  return (
    <Moldura>
      <div className="cg-vitrine">
        <Botao variante="secundaria" onClick={() => irPara("/")}>
          Voltar à vitrine
        </Botao>
        <h2>Solicitação do conjunto de dados</h2>

        {estado.situacao === "registrada" ? (
          <Aviso tipo="sucesso">
            Pedido registrado. Protocolo: {estado.registro.id}. Nada é entregue agora: a
            entrega depende de aprovação de um Admin, que responde até{" "}
            {FORMATADOR.format(new Date(estado.registro.prazo))}, pelo contato que você
            informou — a plataforma não envia e-mail automático.
          </Aviso>
        ) : (
          <form onSubmit={aoEnviar} noValidate>
            <Aviso tipo="atencao">
              A entrega é gratuita, anonimizada e licenciada em CC BY-SA. Depende de aprovação
              de um Admin e é respondida em até 7 dias. Este pedido não entrega nada no ato.
            </Aviso>
            <CampoDeTexto
              rotulo="Solicitante"
              valor={solicitante}
              aoAlterar={definirSolicitante}
              erro={faltando.solicitante ? OBRIGATORIOS : null}
            />
            <CampoDeTexto
              rotulo="Instituição"
              valor={instituicao}
              aoAlterar={definirInstituicao}
              erro={faltando.instituicao ? OBRIGATORIOS : null}
            />
            <CampoDeTexto
              rotulo="E-mail"
              valor={email}
              aoAlterar={definirEmail}
              erro={faltando.email ? OBRIGATORIOS : null}
            />
            <CampoDeTexto
              rotulo="Finalidade declarada"
              valor={finalidade}
              aoAlterar={definirFinalidade}
              erro={faltando.finalidade ? OBRIGATORIOS : null}
              longo
            />
            <CampoDeTexto
              rotulo="Recorte pedido (comunidades, período, tipos de coleta)"
              valor={recorte}
              aoAlterar={definirRecorte}
              erro={faltando.recorte ? OBRIGATORIOS : null}
            />
            {estado.situacao === "falhou" && <Aviso tipo="atencao">{estado.mensagem}</Aviso>}
            <Botao tipo="submit" desabilitado={estado.situacao === "enviando"}>
              Enviar pedido
            </Botao>
          </form>
        )}
      </div>
    </Moldura>
  );
}

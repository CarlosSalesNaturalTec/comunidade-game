import { Aviso, Botao, Moldura } from "comum/react";
import { useState } from "react";
import { enviarParticipacao, type Pretensao } from "../api/solicitacoes";
import { CampoDeTexto } from "./CampoDeTexto";
import { useEnvio } from "./useEnvio";

const FORMATADOR = new Intl.DateTimeFormat("pt-BR", { dateStyle: "long" });

interface Props {
  irPara: (destino: string) => void;
}

const OBRIGATORIOS = "Preencha este campo.";

/** Solicitação de participação como Mestre ou Apoiador (`RF-03-27` a
 * `RF-03-31`, PRD-03 §5.4). Só os campos do PRD-03: aporte, comprovante e nick
 * são do pré-cadastro da App 08 (design — decisão 4). */
export function FormularioDeParticipacao({ irPara }: Props) {
  const [nome, definirNome] = useState("");
  const [email, definirEmail] = useState("");
  const [whatsapp, definirWhatsapp] = useState("");
  const [pretensao, definirPretensao] = useState<Pretensao | "">("");
  const [apresentacao, definirApresentacao] = useState("");
  const [instituicao, definirInstituicao] = useState("");
  const [links, definirLinks] = useState("");
  const [faltando, definirFaltando] = useState<Record<string, boolean>>({});

  const { estado, disparar } = useEnvio(() =>
    enviarParticipacao({
      nome_ou_razao_social: nome.trim(),
      email: email.trim(),
      whatsapp: whatsapp.trim(),
      pretensao: pretensao as Pretensao,
      apresentacao: apresentacao.trim(),
      instituicao: instituicao.trim() || undefined,
      links: links.trim() || undefined,
    }),
  );

  function aoEnviar(evento: React.FormEvent) {
    evento.preventDefault();
    const ausentes = {
      nome: !nome.trim(),
      email: !email.trim(),
      whatsapp: !whatsapp.trim(),
      pretensao: !pretensao,
      apresentacao: !apresentacao.trim(),
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
        <h2>Quero ser Mestre ou Apoiador</h2>

        {estado.situacao === "registrada" ? (
          <Aviso tipo="sucesso">
            Pedido registrado. Protocolo: {estado.registro.id}. Um Admin responde até{" "}
            {FORMATADOR.format(new Date(estado.registro.prazo))}, pelo contato que você
            informou — a plataforma não envia e-mail automático.
          </Aviso>
        ) : (
          <form onSubmit={aoEnviar} noValidate>
            <Aviso tipo="atencao">
              Este pedido não cria cadastro nem acesso. Quem avalia é um Admin, em até 7 dias.
            </Aviso>
            <CampoDeTexto
              rotulo="Nome"
              valor={nome}
              aoAlterar={definirNome}
              erro={faltando.nome ? OBRIGATORIOS : null}
            />
            <CampoDeTexto
              rotulo="E-mail"
              valor={email}
              aoAlterar={definirEmail}
              erro={faltando.email ? OBRIGATORIOS : null}
            />
            <CampoDeTexto
              rotulo="WhatsApp"
              valor={whatsapp}
              aoAlterar={definirWhatsapp}
              erro={faltando.whatsapp ? OBRIGATORIOS : null}
            />
            <div className="cg-campo">
              <label htmlFor="pretensao">Quero ser</label>
              <select
                id="pretensao"
                value={pretensao}
                onChange={(e) => definirPretensao(e.target.value as Pretensao | "")}
                aria-invalid={faltando.pretensao ? true : undefined}
              >
                <option value="">Escolha…</option>
                <option value="mestre">Mestre</option>
                <option value="apoiador">Apoiador</option>
              </select>
              {faltando.pretensao && (
                <p role="alert" className="cg-campo__erro">
                  {OBRIGATORIOS}
                </p>
              )}
            </div>
            <CampoDeTexto
              rotulo="Apresentação"
              valor={apresentacao}
              aoAlterar={definirApresentacao}
              erro={faltando.apresentacao ? OBRIGATORIOS : null}
              longo
            />
            <CampoDeTexto
              rotulo="Instituição que representa (opcional)"
              valor={instituicao}
              aoAlterar={definirInstituicao}
            />
            <CampoDeTexto
              rotulo="Links que comprovem (opcional)"
              valor={links}
              aoAlterar={definirLinks}
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

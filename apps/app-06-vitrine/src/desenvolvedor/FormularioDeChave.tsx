import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import { enviarSolicitacaoDeChave } from "../api/desenvolvedor";
import { CampoDeTexto } from "../formularios/CampoDeTexto";
import { useEnvio } from "../formularios/useEnvio";

const FORMATADOR = new Intl.DateTimeFormat("pt-BR", { dateStyle: "long" });
const OBRIGATORIO = "Preencha este campo.";

/** Solicitação de chave (`RF-03-73`, `RF-03-74`, `RN-03-32`). **Sem espera
 * crescente**: esta é a única superfície pública sem freio por origem, porque
 * nova solicitação é sempre possível (`RN-03-35`) — e por isso a tela não
 * anuncia espera nenhuma. */
export function FormularioDeChave() {
  const [solicitante, definirSolicitante] = useState("");
  const [contato, definirContato] = useState("");
  const [instituicao, definirInstituicao] = useState("");
  const [construir, definirConstruir] = useState("");
  const [faltando, definirFaltando] = useState<Record<string, boolean>>({});

  const { estado, disparar } = useEnvio(() =>
    enviarSolicitacaoDeChave({
      solicitante: solicitante.trim(),
      contato: contato.trim(),
      o_que_pretende_construir: construir.trim(),
      ...(instituicao.trim() ? { instituicao: instituicao.trim() } : {}),
    }),
  );

  function aoEnviar(evento: React.FormEvent) {
    evento.preventDefault();
    const ausentes = {
      solicitante: !solicitante.trim(),
      contato: !contato.trim(),
      construir: !construir.trim(),
    };
    definirFaltando(ausentes);
    if (Object.values(ausentes).some(Boolean)) return;
    void disparar();
  }

  return (
    <section aria-labelledby="cg-formulario-de-chave">
      <h3 id="cg-formulario-de-chave">Peça a sua chave</h3>

      {estado.situacao === "registrada" ? (
        <Aviso tipo="sucesso">
          Pedido registrado. Protocolo: {estado.registro.id}. Nenhuma chave foi emitida agora:
          um Admin avalia e responde até {FORMATADOR.format(new Date(estado.registro.prazo))},
          pelo contato que você informou.
        </Aviso>
      ) : (
        <form onSubmit={aoEnviar} noValidate>
          <Aviso tipo="atencao">
            Enviar este formulário <strong>não emite chave nenhuma e não cria cadastro</strong>
            : ele registra um pedido na fila de avaliação da gestão. Quem avalia e emite a
            chave é um Admin, que responde em até 7 dias.
          </Aviso>
          <CampoDeTexto
            rotulo="Quem é você"
            valor={solicitante}
            aoAlterar={definirSolicitante}
            erro={faltando.solicitante ? OBRIGATORIO : undefined}
          />
          <CampoDeTexto
            rotulo="Contato para a resposta"
            valor={contato}
            aoAlterar={definirContato}
            erro={faltando.contato ? OBRIGATORIO : undefined}
          />
          <CampoDeTexto
            rotulo="Instituição (opcional)"
            valor={instituicao}
            aoAlterar={definirInstituicao}
          />
          <CampoDeTexto
            rotulo="O que você pretende construir"
            valor={construir}
            aoAlterar={definirConstruir}
            longo
            erro={faltando.construir ? OBRIGATORIO : undefined}
          />
          {estado.situacao === "falhou" ? <Aviso tipo="erro">{estado.mensagem}</Aviso> : null}
          <Botao tipo="submit" desabilitado={estado.situacao === "enviando"}>
            Enviar o pedido
          </Botao>
        </form>
      )}
    </section>
  );
}

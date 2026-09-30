import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Moldura } from "comum/react";
import { useState } from "react";
import { apresentarUrlDaChave } from "../api/desenvolvedor";
import { CampoDeTexto } from "../formularios/CampoDeTexto";
import { navegarPara } from "../navegacao/navegar";

const OBRIGATORIO = "Preencha este campo.";

interface Props {
  irPara?: (destino: string) => void;
}

/** Apresentação da URL do que foi construído, dentro do prazo (`RF-03-77`).
 * Quem prova a titularidade é o **identificador** da chave, entregue na
 * emissão: o segredo nunca é pedido aqui (`RN-01-33`). A recusa que o núcleo
 * declarar — prazo vencido, chave inexistente — aparece como o que é, e nunca
 * disfarçada (documento 99 §6 invariante 25). */
export function ApresentacaoDaUrl({ irPara = navegarPara }: Props) {
  const [chaveId, definirChaveId] = useState("");
  const [url, definirUrl] = useState("");
  const [faltando, definirFaltando] = useState<Record<string, boolean>>({});
  const [estado, definirEstado] = useState<
    | { situacao: "preenchendo" }
    | { situacao: "apresentada" }
    | { situacao: "recusada"; mensagem: string }
  >({ situacao: "preenchendo" });

  async function aoEnviar(evento: React.FormEvent) {
    evento.preventDefault();
    const ausentes = { chaveId: !chaveId.trim(), url: !url.trim() };
    definirFaltando(ausentes);
    if (Object.values(ausentes).some(Boolean)) return;

    try {
      await apresentarUrlDaChave(chaveId.trim(), url.trim());
      definirEstado({ situacao: "apresentada" });
    } catch (erro) {
      definirEstado({
        situacao: "recusada",
        mensagem:
          erro instanceof ErroDaApi
            ? erro.message
            : "Não foi possível apresentar a URL agora. O que você preencheu continua aqui; tente de novo.",
      });
    }
  }

  return (
    <Moldura>
      <div className="cg-vitrine">
        <Botao variante="secundaria" onClick={() => irPara("/desenvolvedor")}>
          Voltar à Área do Apoiador Desenvolvedor
        </Botao>
        <h2>Apresentar a URL do que você construiu</h2>

        {estado.situacao === "apresentada" ? (
          <Aviso tipo="sucesso">
            URL apresentada. A sua chave segue válida — a apresentação dentro do prazo é o que
            evita a revogação.
          </Aviso>
        ) : (
          <form onSubmit={(evento) => void aoEnviar(evento)} noValidate>
            <Aviso tipo="atencao">
              Informe o <strong>identificador</strong> da chave, o que veio na emissão junto
              com o segredo. O segredo não é pedido aqui, e nunca deve ser compartilhado.
            </Aviso>
            <CampoDeTexto
              rotulo="Identificador da chave"
              valor={chaveId}
              aoAlterar={definirChaveId}
              erro={faltando.chaveId ? OBRIGATORIO : undefined}
            />
            <CampoDeTexto
              rotulo="URL do que você construiu"
              valor={url}
              aoAlterar={definirUrl}
              erro={faltando.url ? OBRIGATORIO : undefined}
            />
            {estado.situacao === "recusada" ? (
              <Aviso tipo="erro">{estado.mensagem}</Aviso>
            ) : null}
            <Botao tipo="submit">Apresentar a URL</Botao>
          </form>
        )}
      </div>
    </Moldura>
  );
}

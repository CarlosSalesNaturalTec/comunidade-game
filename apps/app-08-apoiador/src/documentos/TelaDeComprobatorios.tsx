import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { type DocumentoDoApoiador, declararDocumento, listarMeusDocumentos } from "./api";

// Envia currículo, portfólio, rede social, termo de doação ou comprovante
// por endereço e rótulo — nunca anexo de arquivo —, declara antes do envio
// que só um Admin o publica, e separa o que já está publicado do que segue
// pendente (`RF-14-18` a `RF-14-20`, `RN-14-12`, PRD-14 §5.9).
export function TelaDeComprobatorios() {
  const { sessao } = useSessao();
  const [documentos, definirDocumentos] = useState<DocumentoDoApoiador[]>([]);
  const [carregando, definirCarregando] = useState(true);

  const [endereco, definirEndereco] = useState("");
  const [rotulo, definirRotulo] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  const carregarDocumentos = useCallback(async () => {
    if (!sessao) return;
    definirCarregando(true);
    try {
      definirDocumentos(await listarMeusDocumentos(sessao.token));
    } finally {
      definirCarregando(false);
    }
  }, [sessao]);

  useEffect(() => {
    carregarDocumentos();
  }, [carregarDocumentos]);

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirEnviando(true);
    definirErro(null);
    definirSucesso(false);
    try {
      await declararDocumento({ endereco, rotulo }, sessao.token);
      definirEndereco("");
      definirRotulo("");
      definirSucesso(true);
      await carregarDocumentos();
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível declarar o documento. Tente novamente.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  const publicados = documentos.filter((documento) => documento.publicado);
  const pendentes = documentos.filter((documento) => !documento.publicado);

  return (
    <Moldura>
      <Cabecalho
        titulo="Documentos comprobatórios"
        subtitulo="Currículo, portfólio, rede social, termo de doação ou comprovante — sempre um link."
      />

      <AvisoDeColeta dado="o endereço e o rótulo do documento comprobatório" />

      <form onSubmit={aoEnviar}>
        <Campo rotulo="Endereço (link)" valor={endereco} aoAlterar={definirEndereco} />
        <Campo rotulo="Rótulo" valor={rotulo} aoAlterar={definirRotulo} />
        <p>
          Este documento entra na fila da gestão e só aparece na sua página pública quando um
          Admin o anexar ao cadastro.
        </p>
        <Botao tipo="submit" desabilitado={enviando}>
          Enviar documento
        </Botao>
      </form>
      {enviando && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {sucesso && <Aviso tipo="sucesso">Documento enviado como pendente.</Aviso>}

      {!carregando && (
        <>
          <section>
            <h2>Publicados</h2>
            {publicados.length === 0 ? (
              <p>Nenhum documento publicado ainda.</p>
            ) : (
              <ul>
                {publicados.map((documento) => (
                  <li key={documento.id}>
                    {documento.rotulo} — {documento.endereco}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section>
            <h2>Pendentes</h2>
            {pendentes.length === 0 ? (
              <p>Nenhum documento pendente.</p>
            ) : (
              <ul>
                {pendentes.map((documento) => (
                  <li key={documento.id}>
                    {documento.rotulo} — {documento.endereco}
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}
    </Moldura>
  );
}

import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { ofertarItem } from "./api";

// A oferta do Apoiador: nome, tipo de recurso, quantidade, comunidade e
// ponto de apoio por identificador — sem campo de preço, porque o preço vem
// sempre da tabela de referência da gestão, e o item entra pendente até a
// homologação do Admin (`RF-14-77` a `RF-14-79`, `RN-14-42`, `RN-14-43`).
export function TelaDeOferta() {
  const { sessao } = useSessao();
  const [nome, definirNome] = useState("");
  const [tipoDeRecursoId, definirTipoDeRecursoId] = useState("");
  const [estoque, definirEstoque] = useState("1");
  const [comunidadeId, definirComunidadeId] = useState("");
  const [pontoDeApoioId, definirPontoDeApoioId] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirEnviando(true);
    definirErro(null);
    definirSucesso(false);
    try {
      await ofertarItem(
        {
          nome,
          tipo_de_recurso_id: tipoDeRecursoId,
          estoque: Number(estoque),
          comunidade_virtual_id: comunidadeId,
          ponto_de_apoio_id: pontoDeApoioId,
        },
        sessao.token,
      );
      definirSucesso(true);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível registrar a oferta. Tente novamente.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Ofertar item"
        subtitulo="Um item para o catálogo avulso, com o ponto de apoio que o lastreia."
      />
      <AvisoDeColeta dado="a oferta de item ao catálogo avulso" />
      <Aviso tipo="atencao">
        O preço em pontos extras vem da tabela de referência da gestão — não se declara aqui. O
        item entra pendente e só aparece no catálogo depois de homologado por um Admin.
      </Aviso>
      <form onSubmit={aoEnviar}>
        <Campo rotulo="Nome" valor={nome} aoAlterar={definirNome} />
        <Campo
          rotulo="Tipo de recurso"
          valor={tipoDeRecursoId}
          aoAlterar={definirTipoDeRecursoId}
        />
        <Campo rotulo="Quantidade" tipo="number" valor={estoque} aoAlterar={definirEstoque} />
        <Campo rotulo="Comunidade" valor={comunidadeId} aoAlterar={definirComunidadeId} />
        <Campo
          rotulo="Ponto de apoio"
          valor={pontoDeApoioId}
          aoAlterar={definirPontoDeApoioId}
        />

        <Botao tipo="submit" desabilitado={enviando}>
          Ofertar item
        </Botao>
      </form>
      {enviando && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {sucesso && (
        <Aviso tipo="sucesso">
          Oferta registrada. Acompanhe a homologação em "Minhas ofertas".
        </Aviso>
      )}
    </Moldura>
  );
}

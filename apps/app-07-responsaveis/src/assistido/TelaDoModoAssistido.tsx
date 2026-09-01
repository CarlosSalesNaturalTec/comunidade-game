import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { ProvedorDeDireitos } from "../direitos/ContextoDeDireitos";
import type { CatalogoDeTermo } from "../termos/api";
import { consultarTermos } from "../termos/api";
import {
  type GuerreiroVinculavel,
  listarGuerreirosVinculaveis,
  listarResponsaveisDoGuerreiro,
  type ResponsavelVinculado,
  registrarAutorizacaoAssistida,
} from "./api";

// O modo assistido: um Admin ou um Mestre, com o responsável presente,
// escolhe o Guerreiro(a) e qual dos responsáveis vinculados está aqui,
// percorre com ele o texto do termo e registra a decisão em nome dele,
// com a mesma força do ato do próprio — quem opera também testemunha, no
// mesmo precedente do termo impresso da biometria (`RF-13-35`, `RF-13-36`,
// `RF-13-38`, `RN-13-16`, design — decisão 5). Alcança só esta decisão:
// nada de evolução, solicitações, transparência ou histórico de acessos.
export function TelaDoModoAssistido() {
  const { sessao, sair } = useSessao();

  const [guerreiros, definirGuerreiros] = useState<GuerreiroVinculavel[] | null>(null);
  const [filtro, definirFiltro] = useState("");
  const [guerreiroId, definirGuerreiroId] = useState<string | null>(null);

  const [responsaveis, definirResponsaveis] = useState<ResponsavelVinculado[] | null>(null);
  const [responsavelId, definirResponsavelId] = useState<string | null>(null);

  const [termo, definirTermo] = useState<CatalogoDeTermo | null>(null);

  const [registrando, definirRegistrando] = useState(false);
  const [confirmacao, definirConfirmacao] = useState<string | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarGuerreirosVinculaveis(sessao.token)
      .then(definirGuerreiros)
      .catch(() => definirErro("Não foi possível carregar os Guerreiros e Guerreiras."));
    consultarTermos(sessao.token)
      .then((catalogo) => definirTermo(catalogo[0] ?? null))
      .catch(() => definirErro("Não foi possível carregar o termo."));
  }, [sessao]);

  useEffect(() => {
    if (!sessao || !guerreiroId) {
      definirResponsaveis(null);
      definirResponsavelId(null);
      return;
    }
    definirResponsaveis(null);
    definirResponsavelId(null);
    definirConfirmacao(null);
    listarResponsaveisDoGuerreiro(guerreiroId, sessao.token)
      .then(definirResponsaveis)
      .catch(() => definirErro("Não foi possível carregar os responsáveis."));
  }, [guerreiroId, sessao]);

  async function registrar(decisao: "concede" | "nega") {
    if (!sessao || !guerreiroId || !responsavelId) return;
    definirRegistrando(true);
    definirErro(null);
    definirConfirmacao(null);
    try {
      // Quem opera testemunha o próprio ato — mesmo precedente do termo
      // impresso da biometria (`TelaDoTermo` da App 01).
      await registrarAutorizacaoAssistida(
        guerreiroId,
        responsavelId,
        decisao,
        sessao.persona_id,
        sessao.token,
      );
      definirConfirmacao(
        decisao === "concede"
          ? "Concessão registrada em nome do responsável — mesma força do ato feito por ele."
          : "Recusa registrada em nome do responsável — mesma força do ato feito por ele.",
      );
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível registrar o ato. Tente novamente.",
      );
    } finally {
      definirRegistrando(false);
    }
  }

  const guerreirosFiltrados = (guerreiros ?? []).filter((guerreiro) =>
    guerreiro.nick.toLowerCase().includes(filtro.toLowerCase()),
  );

  return (
    <ProvedorDeDireitos irParaTransparencia={() => {}}>
      <Moldura>
        <Cabecalho titulo="Atendimento assistido" acao={{ rotulo: "Sair", aoAcionar: sair }} />
        <Aviso tipo="atencao">
          Use este modo só com o responsável presente. O que é registrado aqui vale como se ele
          tivesse feito sozinho.
        </Aviso>
        <AvisoDeColeta dado="a decisão da autorização única, em nome do responsável presente" />

        <section>
          <h2>1. Escolha o Guerreiro(a)</h2>
          <div className="cg-campo">
            <label htmlFor="filtro-de-guerreiro">Buscar por apelido</label>
            <input
              id="filtro-de-guerreiro"
              value={filtro}
              onChange={(evento) => definirFiltro(evento.target.value)}
            />
          </div>
          {guerreiros === null && <EstadoDaLista>Carregando…</EstadoDaLista>}
          {guerreiros !== null && (
            <ul aria-label="Guerreiros e Guerreiras">
              {guerreirosFiltrados.map((guerreiro) => (
                <li key={guerreiro.id}>
                  <Botao
                    variante={guerreiro.id === guerreiroId ? "primaria" : "secundaria"}
                    onClick={() => definirGuerreiroId(guerreiro.id)}
                  >
                    {guerreiro.nick}
                  </Botao>
                </li>
              ))}
            </ul>
          )}
        </section>

        {guerreiroId && (
          <section>
            <h2>2. Quem está presente</h2>
            {responsaveis === null && <EstadoDaLista>Carregando…</EstadoDaLista>}
            {responsaveis !== null && responsaveis.length === 0 && (
              <EstadoDaLista>Nenhum responsável vinculado a este Guerreiro(a).</EstadoDaLista>
            )}
            {responsaveis !== null && responsaveis.length > 0 && (
              <ul aria-label="Responsáveis vinculados">
                {responsaveis.map((responsavel) => (
                  <li key={responsavel.id}>
                    <Botao
                      variante={responsavel.id === responsavelId ? "primaria" : "secundaria"}
                      onClick={() => definirResponsavelId(responsavel.id)}
                    >
                      {responsavel.nome} — {responsavel.grau_de_parentesco}
                    </Botao>
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}

        {responsavelId && termo && (
          <section aria-label="Termo da autorização única">
            <h2>3. Percorra o termo com o responsável</h2>
            <p style={{ whiteSpace: "pre-line" }}>{termo.vigente.texto}</p>
          </section>
        )}

        {responsavelId && (
          <section>
            <h2>4. Registrar a decisão</h2>
            <p>
              Ao confirmar, o ato entra em nome do responsável presente, com você como quem
              operou e testemunhou.
            </p>
            <Botao onClick={() => registrar("concede")} desabilitado={registrando}>
              Conceder
            </Botao>
            <Botao
              variante="secundaria"
              onClick={() => registrar("nega")}
              desabilitado={registrando}
            >
              Recusar
            </Botao>
            {confirmacao && <Aviso tipo="sucesso">{confirmacao}</Aviso>}
            {erro && <Aviso tipo="erro">{erro}</Aviso>}
          </section>
        )}
      </Moldura>
    </ProvedorDeDireitos>
  );
}

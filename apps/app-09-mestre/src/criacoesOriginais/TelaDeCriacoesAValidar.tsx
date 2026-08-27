import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  type CriacaoNaFila,
  devolverCriacaoOriginal,
  listarFilaDeCriacoes,
  validarCriacaoOriginal,
} from "./api";

// A fila das criações originais entregues nas trilhas do Mestre autor —
// validar credita a autoria e libera o badge; devolver exige o motivo em
// linguagem simples, e a autoria nunca muda (`RF-09-31`, `RF-09-32`,
// `RF-09-34`, `RN-09-04`). A App 09 nunca oferece editar a produção nem
// reatribuir a autoria.
export function TelaDeCriacoesAValidar() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [fila, definirFila] = useState<CriacaoNaFila[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [decidindo, definirDecidindo] = useState<string | null>(null);
  const [motivoPorCriacao, definirMotivoPorCriacao] = useState<Record<string, string>>({});
  const [ultimaValidada, definirUltimaValidada] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const resultado = await listarFilaDeCriacoes(sessao.token);
      definirFila(resultado);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a fila agora. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function validar(criacao: CriacaoNaFila) {
    if (!sessao) return;
    definirDecidindo(criacao.id);
    definirErro(null);
    try {
      await validarCriacaoOriginal(criacao.id, sessao.token);
      definirFila((atual) => (atual ?? []).filter((item) => item.id !== criacao.id));
      definirUltimaValidada(criacao.id);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível validar agora. Tente novamente em instantes.");
    } finally {
      definirDecidindo(null);
    }
  }

  async function devolver(criacao: CriacaoNaFila) {
    if (!sessao) return;
    const motivo = (motivoPorCriacao[criacao.id] ?? "").trim();
    if (!motivo) {
      definirErro("Escreva o motivo antes de devolver.");
      return;
    }
    definirDecidindo(criacao.id);
    definirErro(null);
    try {
      await devolverCriacaoOriginal(criacao.id, motivo, sessao.token);
      definirFila((atual) => (atual ?? []).filter((item) => item.id !== criacao.id));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível devolver agora. Tente novamente em instantes.");
    } finally {
      definirDecidindo(null);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Criações originais a validar"
        acao={{ rotulo: "Sair", aoAcionar: sair }}
      />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {fila === null && <EstadoDaLista>Carregando a fila…</EstadoDaLista>}
      {fila !== null && fila.length === 0 && (
        <EstadoDaLista>Nenhuma criação original esperando decisão.</EstadoDaLista>
      )}
      {fila !== null && fila.length > 0 && (
        <ul className="lista-de-criacoes-a-validar" aria-label="Criações a validar">
          {fila.map((criacao) => (
            <li key={criacao.id} className="lista-de-criacoes-a-validar__item">
              <p>
                <strong>{criacao.trilha_nome}</strong>
              </p>
              <p>Critério de validação: {criacao.criterio_de_validacao}</p>
              <p>{criacao.producao ?? "Produção em mídia enviada."}</p>
              <ul aria-label="Autoria">
                {criacao.autores.map((autor) => (
                  <li key={autor.nick}>
                    {autor.nick}
                    {autor.papel && ` — ${autor.papel}`}
                  </li>
                ))}
              </ul>

              <Botao onClick={() => validar(criacao)} desabilitado={decidindo === criacao.id}>
                Validar
              </Botao>

              <div className="cg-campo">
                <label htmlFor={`motivo-${criacao.id}`}>Motivo da devolução</label>
                <textarea
                  id={`motivo-${criacao.id}`}
                  value={motivoPorCriacao[criacao.id] ?? ""}
                  onChange={(evento) =>
                    definirMotivoPorCriacao((atual) => ({
                      ...atual,
                      [criacao.id]: evento.target.value,
                    }))
                  }
                />
              </div>
              <Botao
                variante="secundaria"
                onClick={() => devolver(criacao)}
                desabilitado={decidindo === criacao.id}
              >
                Devolver
              </Botao>
            </li>
          ))}
        </ul>
      )}

      {ultimaValidada && (
        <Aviso tipo="sucesso">
          Autoria creditada e badge de autoria liberado. Ela só vai à vitrine pública quando
          todos os creditados tiverem autorização de divulgação vigente do responsável — sem
          ela, ela continua só no portfólio do Guerreiro(a).
        </Aviso>
      )}
    </Moldura>
  );
}

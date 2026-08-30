import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  declararEscolhaDaEquipe,
  type ItemDaProgramacao,
  obterProgramacaoDoEncontro,
} from "../api/programacao";
import { EntregaDaProducao } from "./EntregaDaProducao";
import { EquipeDaTrilha } from "./EquipeDaTrilha";

interface Props {
  equipeId: string;
  token: string;
  aoVoltar: () => void;
  /** Presente só quando quem está na sessão de trabalho do aparelho é o
   * Mestre — autoriza a homologação da equipe da trilha ali mesmo
   * (`RF-04-62`, `RN-04-18`). */
  podeHomologarEquipeDaTrilha?: boolean;
  tokenDeTrabalho?: string | null;
}

const MENSAGEM_SEM_PROGRAMACAO =
  "Este encontro ainda não tem atividade declarada. Peça a um Mestre para verificar.";

const MENSAGEM_SEM_REDE =
  "Não foi possível atualizar a programação agora. O que já foi carregado continua aqui.";

const MENSAGEM_ESCOLHA_INDISPONIVEL =
  "A escolha está indisponível sem rede. Assim que a rede voltar, você pode escolher.";

// O caminho das trilhas da tela inicial: da equipe escolhida à programação
// do encontro — missão, conteúdo e atividade do dia (`RF-04-35`). A
// programação é lista e a equipe é quem escolhe em qual trabalhar,
// declarando a escolha ao núcleo — a aplicação nunca decide por conta
// própria quando há mais de uma atividade (`RF-02-42`, `RF-04-58`,
// documento 05 §4, documento 02 §5).
export function TelaDaProgramacao({
  equipeId,
  token,
  aoVoltar,
  podeHomologarEquipeDaTrilha = false,
  tokenDeTrabalho = null,
}: Props) {
  const [itens, definirItens] = useState<ItemDaProgramacao[] | null>(null);
  const [semRede, definirSemRede] = useState(false);
  const [idExibido, definirIdExibido] = useState<string | null>(null);
  const [declarando, definirDeclarando] = useState(false);
  const declaradaSozinhaRef = useRef<string | null>(null);

  const carregar = useCallback(async () => {
    try {
      const proximos = await obterProgramacaoDoEncontro(equipeId, token);
      definirItens(proximos);
      definirSemRede(false);
      const corrente = proximos.find((item) => item.corrente);
      definirIdExibido((atual) => {
        if (atual && proximos.some((item) => item.atividade.id === atual)) return atual;
        if (corrente) return corrente.atividade.id;
        if (proximos.length === 1) return proximos[0].atividade.id;
        return null;
      });
    } catch {
      // O conteúdo já carregado permanece na tela — a leitura é dado, não
      // fato a sincronizar, e nunca vai para fila de reenvio (`RF-04-58`).
      definirSemRede(true);
    }
  }, [equipeId, token]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const declarar = useCallback(
    async (atividadeId: string) => {
      if (semRede) return;
      definirDeclarando(true);
      try {
        await declararEscolhaDaEquipe(equipeId, atividadeId, token);
        definirItens((atual) =>
          atual
            ? atual.map((item) => ({ ...item, corrente: item.atividade.id === atividadeId }))
            : atual,
        );
        definirIdExibido(atividadeId);
      } catch {
        definirSemRede(true);
      } finally {
        definirDeclarando(false);
      }
    },
    [equipeId, token, semRede],
  );

  // Uma única atividade não é escolha: nada a decidir por conta própria, e
  // sem a declaração o campo do painel do dia nasceria sempre vazio.
  useEffect(() => {
    if (itens?.length !== 1 || semRede) return;
    const unica = itens[0];
    if (unica.corrente || declaradaSozinhaRef.current === unica.atividade.id) return;
    declaradaSozinhaRef.current = unica.atividade.id;
    declarar(unica.atividade.id);
  }, [itens, semRede, declarar]);

  if (itens === null && !semRede) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Programação do encontro"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <EstadoDaLista>Carregando a programação…</EstadoDaLista>
      </Moldura>
    );
  }

  const item = itens?.find((candidato) => candidato.atividade.id === idExibido) ?? null;

  return (
    <Moldura>
      <Cabecalho
        titulo="Programação do encontro"
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      <Botao variante="secundaria" onClick={carregar}>
        Atualizar
      </Botao>
      {semRede && <Aviso tipo="atencao">{MENSAGEM_SEM_REDE}</Aviso>}

      {itens !== null && itens.length === 0 && (
        <Aviso tipo="atencao">{MENSAGEM_SEM_PROGRAMACAO}</Aviso>
      )}

      {itens !== null && itens.length > 1 && (
        <nav aria-label="Atividades do encontro">
          <ul className="cg-escolha-de-atividade">
            {itens.map((candidato) => (
              <li key={candidato.atividade.id}>
                <Botao
                  variante={candidato.corrente ? "primaria" : "secundaria"}
                  onClick={() => declarar(candidato.atividade.id)}
                  desabilitado={declarando || semRede}
                >
                  {candidato.missao_titulo} — {candidato.atividade.titulo}
                </Botao>
              </li>
            ))}
          </ul>
          {semRede && <Aviso tipo="atencao">{MENSAGEM_ESCOLHA_INDISPONIVEL}</Aviso>}
        </nav>
      )}

      {item && (
        <section aria-label="Missão do dia">
          <h2>{item.missao_titulo}</h2>

          <h3>Conteúdo</h3>
          <ul aria-label="Conteúdo da missão">
            {item.conteudos.map((conteudo) => (
              <li key={conteudo.id}>
                {conteudo.tipo === "texto" && <p>{conteudo.corpo}</p>}
                {conteudo.tipo === "link_externo" && (
                  <a href={conteudo.endereco ?? "#"} target="_blank" rel="noreferrer">
                    {conteudo.endereco}
                  </a>
                )}
                {conteudo.tipo === "imagem" && conteudo.referencia && (
                  <img src={conteudo.referencia} alt="" />
                )}
                {conteudo.tipo === "video" && conteudo.referencia && (
                  // biome-ignore lint/a11y/useMediaCaption: legenda é conteúdo do Mestre autor, fora desta fatia.
                  <video src={conteudo.referencia} controls />
                )}
                {conteudo.tipo === "arquivo" && conteudo.referencia && (
                  <a href={conteudo.referencia}>Arquivo de apoio</a>
                )}
                {conteudo.autoria === "terceiro" && conteudo.fonte && (
                  <p className="cg-fonte-do-conteudo">Fonte: {conteudo.fonte}</p>
                )}
              </li>
            ))}
          </ul>

          <h3>Atividade do dia</h3>
          <p>{item.atividade.titulo}</p>
          {item.atividade.descricao && <p>{item.atividade.descricao}</p>}
          <p>{item.atividade.producao_esperada}</p>

          {item.bibliografia.length > 0 && (
            <>
              <h3>Bibliografia</h3>
              <ul aria-label="Bibliografia da missão">
                {item.bibliografia.map((entrada) => (
                  <li key={entrada.id}>
                    {entrada.titulo} — {entrada.capitulo}
                    {entrada.apoiador_nome && <> · doado por {entrada.apoiador_nome}</>}
                  </li>
                ))}
              </ul>
            </>
          )}

          <EquipeDaTrilha
            trilhaId={item.trilha_id}
            trilhaTitulo={item.trilha_titulo}
            tokenDoGuerreiro={token}
            podeHomologar={podeHomologarEquipeDaTrilha}
            tokenDeTrabalho={tokenDeTrabalho}
          />

          <EntregaDaProducao
            equipeId={equipeId}
            token={token}
            producaoEsperada={item.atividade.producao_esperada}
          />
        </section>
      )}
    </Moldura>
  );
}

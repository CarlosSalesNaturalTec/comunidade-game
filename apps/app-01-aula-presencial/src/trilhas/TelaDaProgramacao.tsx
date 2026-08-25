import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type ItemDaProgramacao, obterProgramacaoDoEncontro } from "../api/programacao";

interface Props {
  equipeId: string;
  token: string;
  aoVoltar: () => void;
}

const MENSAGEM_SEM_PROGRAMACAO =
  "Este encontro ainda não tem atividade declarada. Peça a um Mestre para verificar.";

const MENSAGEM_SEM_REDE =
  "Não foi possível atualizar a programação agora. O que já foi carregado continua aqui.";

// O caminho das trilhas da tela inicial: da equipe escolhida à programação
// do encontro — missão, conteúdo e atividade do dia (`RF-04-35`). A
// programação é lista e a escolha entre atividades é estado deste
// aparelho, nunca enviada ao núcleo (documento 05 §4, documento 02 §5).
export function TelaDaProgramacao({ equipeId, token, aoVoltar }: Props) {
  const [itens, definirItens] = useState<ItemDaProgramacao[] | null>(null);
  const [semRede, definirSemRede] = useState(false);
  const [atividadeEscolhidaId, definirAtividadeEscolhidaId] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    try {
      const proximos = await obterProgramacaoDoEncontro(equipeId, token);
      definirItens(proximos);
      definirSemRede(false);
      definirAtividadeEscolhidaId((atual) =>
        atual && proximos.some((item) => item.atividade.id === atual)
          ? atual
          : (proximos[0]?.atividade.id ?? null),
      );
    } catch {
      // O conteúdo já carregado permanece na tela — a leitura é dado, não
      // fato a sincronizar, e nunca vai para fila de reenvio (`RF-04-58`).
      definirSemRede(true);
    }
  }, [equipeId, token]);

  useEffect(() => {
    carregar();
  }, [carregar]);

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

  const item =
    itens?.find((candidato) => candidato.atividade.id === atividadeEscolhidaId) ?? null;

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
                  variante={
                    candidato.atividade.id === atividadeEscolhidaId ? "primaria" : "secundaria"
                  }
                  onClick={() => definirAtividadeEscolhidaId(candidato.atividade.id)}
                >
                  {candidato.missao_titulo} — {candidato.atividade.titulo}
                </Botao>
              </li>
            ))}
          </ul>
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
        </section>
      )}
    </Moldura>
  );
}

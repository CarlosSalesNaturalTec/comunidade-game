import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useEffect, useState } from "react";
import { type ConteudoDaMissao, lerArquivoDoConteudo, type MissaoDaTrilha } from "./api";

interface Props {
  missao: MissaoDaTrilha;
  autorNome: string | null;
  onFechar: () => void;
}

// A licença é fixa, a mesma que a leitura pública da trilha já declara
// (documento 03 — código aberto e CC BY-SA); não é parâmetro de operação.
const LICENCA = "CC BY-SA";

// O crédito sem nick cai no mesmo texto de reserva da App 05, para que a
// pré-visualização não invente autor nem o omita (`RF-09-25`).
const CREDITO_SEM_NICK = "Mestre autor";

// Apresenta a missão na mesma ordem e na mesma forma em que o Guerreiro(a) a
// encontrará (`app-05-guerreiro/src/trilha/Missao.tsx`), a partir do que já
// está gravado: a trilha em rascunho não sai pela leitura pública
// (`RF-09-04`), e a pré-visualização nunca grava nem publica nada
// (`RF-09-25`). Ela espelha aquela tela em vez de partilhar componente com
// ela — as duas podem divergir, e é a suíte que segura (design — decisão 4).
export function PreVisualizacaoDaMissao({ missao, autorNome, onFechar }: Props) {
  const conteudos = [...(missao.conteudos ?? [])].sort((a, b) => a.ordem - b.ordem);
  const bibliografia = missao.bibliografia ?? [];
  const perguntas = missao.perguntas_do_desbloqueio ?? [];

  return (
    <section aria-label={`Pré-visualização de ${missao.titulo}`} className="cg-moldura">
      <h2>Pré-visualização — {missao.titulo}</h2>

      {!missao.obrigatoria && (
        <Aviso tipo="andamento">
          Essa missão é opcional — ela não conta no que falta para o próximo nível.
        </Aviso>
      )}

      {conteudos.length === 0 && <p>Nenhum conteúdo escrito ainda.</p>}
      <ul aria-label="Conteúdo da missão">
        {conteudos.map((conteudo) => (
          <li key={conteudo.id}>
            <ConteudoPreVisualizado conteudo={conteudo} tituloDaMissao={missao.titulo} />
            {conteudo.autoria === "terceiro" && conteudo.fonte && (
              <p>Fonte: {conteudo.fonte}</p>
            )}
          </li>
        ))}
      </ul>

      <p>
        Crédito: {autorNome ?? CREDITO_SEM_NICK} — licença {LICENCA}
      </p>

      <h3>Bibliografia</h3>
      {bibliografia.length === 0 && <p>Nenhuma bibliografia declarada ainda.</p>}
      <ul aria-label="Bibliografia da missão">
        {bibliografia.map((entrada) => (
          <li key={entrada.id}>
            {entrada.titulo} — {entrada.capitulo}
          </li>
        ))}
      </ul>

      {/* As atividades são como o Guerreiro(a) entrega a produção: sem elas,
          a pré-visualização mostra menos do que ele verá (`RF-09-25`). */}
      <h3>Atividades</h3>
      {missao.atividades.length === 0 && <p>Nenhuma atividade declarada ainda.</p>}
      <ul aria-label="Atividades da missão">
        {missao.atividades.map((atividade) => (
          <li key={atividade.id}>
            {atividade.titulo} — {atividade.producao_esperada}
          </li>
        ))}
      </ul>

      <h3>{missao.e_sondagem ? "Sondagem" : "Desafio de desbloqueio"}</h3>
      {missao.tipo_do_desafio_de_desbloqueio == null && (
        <p>
          {missao.e_sondagem
            ? "Sondagem ainda sem perguntas."
            : "Ainda sem desafio de desbloqueio."}
        </p>
      )}
      {missao.tipo_do_desafio_de_desbloqueio === "pratico" && (
        <p>{missao.desafio_de_desbloqueio_enunciado}</p>
      )}
      {missao.tipo_do_desafio_de_desbloqueio === "quiz" && (
        // Em leitura: o enunciado e as alternativas como o Guerreiro(a) as
        // lerá, sem a indicação de qual é a correta, que é do autor.
        <ol aria-label="Perguntas do desbloqueio">
          {perguntas.map((pergunta) => (
            <li key={pergunta.id}>
              {pergunta.enunciado}
              <ul>
                {pergunta.alternativas.map((alternativa) => (
                  <li key={alternativa}>{alternativa}</li>
                ))}
              </ul>
            </li>
          ))}
        </ol>
      )}

      <Botao onClick={onFechar}>Fechar pré-visualização</Botao>
    </section>
  );
}

// Texto e link saem do próprio conteúdo; imagem, vídeo e arquivo vêm em
// bytes do núcleo, porque toda rota sob `/v1` exige a chave da aplicação em
// cabeçalho e `<img src>` não a manda (`RF-09-25`, design — decisão 6).
// Antes desta leitura, os três apareciam como a frase "Arquivo enviado.".
function ConteudoPreVisualizado({
  conteudo,
  tituloDaMissao,
}: {
  conteudo: ConteudoDaMissao;
  tituloDaMissao: string;
}) {
  const { sessao } = useSessao();
  const token = sessao?.token ?? null;
  const [endereco, definirEndereco] = useState<string | null>(null);
  const [naoAbriu, definirNaoAbriu] = useState(false);

  const temArquivo = conteudo.referencia !== null;
  const ehArquivo =
    conteudo.tipo === "imagem" || conteudo.tipo === "video" || conteudo.tipo === "arquivo";

  useEffect(() => {
    if (!token || !ehArquivo || !temArquivo) return;
    let local: string | null = null;
    let descartado = false;
    lerArquivoDoConteudo(conteudo.id, token)
      .then((bytes) => {
        if (descartado) return;
        local = URL.createObjectURL(bytes);
        definirEndereco(local);
      })
      .catch(() => {
        if (!descartado) definirNaoAbriu(true);
      });
    return () => {
      descartado = true;
      if (local) URL.revokeObjectURL(local);
    };
  }, [conteudo.id, token, ehArquivo, temArquivo]);

  if (conteudo.tipo === "texto") return <p>{conteudo.corpo}</p>;
  if (conteudo.tipo === "link_externo") {
    return <a href={conteudo.endereco ?? "#"}>{conteudo.endereco}</a>;
  }

  // Envio não concluído é dito pendente, nunca apresentado como quebrado.
  if (!temArquivo) return <p>Envio ainda não concluído.</p>;
  if (naoAbriu) {
    return <Aviso tipo="atencao">Esse arquivo não abriu agora, mas segue anexado.</Aviso>;
  }
  if (!endereco) return <p>Carregando o arquivo…</p>;

  if (conteudo.tipo === "imagem") {
    return (
      <img
        src={endereco}
        alt={`Conteúdo de ${tituloDaMissao}`}
        onError={() => definirNaoAbriu(true)}
      />
    );
  }
  if (conteudo.tipo === "video") {
    // biome-ignore lint/a11y/useMediaCaption: legenda do vídeo do Mestre não é declarada no Ciclo 01 — o PRD-09 não a prevê, e inventar faixa vazia não ajuda quem não ouve.
    return <video src={endereco} controls aria-label={`Vídeo de ${tituloDaMissao}`} />;
  }
  return <a href={endereco}>Abrir o arquivo de apoio</a>;
}

import { type ReactNode, useEffect, useState } from "react";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { useNarracao } from "../narracao/ProvedorDeNarracao";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { EstadoDaLista } from "../react/EstadoDaLista";
import { MidiaDoNucleo } from "../react/MidiaDoNucleo";
import { SequenciaPaginada } from "../react/SequenciaPaginada";
import {
  type AtividadeDaMissaoPublica,
  lerArquivoDoConteudo,
  type MissaoNoPercurso,
  type MissaoPublica,
} from "./api";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";
import { Sondagem } from "./Sondagem";

interface Props {
  missao: MissaoNoPercurso;
  /** O dado público da missão, buscado pelo `GuiaDaTrilha`: a missão não
   * busca mais nada, porque a bibliografia e o crédito — que saíam da mesma
   * resposta — passaram a ser dele (design — decisão 1). */
  missaoPublica: MissaoPublica | undefined;
  /** A falha da busca, dita por quem buscou. */
  erroDoConteudo?: string | null;
  aoDesbloquear: () => void;
  /** Liga a submissão do desbloqueio, que carrega a sondagem com ela — as
   * duas aplicações a ligam (design — decisão 3). */
  submissaoDoDesbloqueioLigada?: boolean;
  /** A entrega individual da produção, ligada por quem a oferece. A App 01
   * NUNCA a liga: a entrega dela é por equipe, no caminho das equipes
   * (`RF-04-45`, `RF-05-74`, design — decisão 3). */
  entregaDaProducao?: (dados: {
    missaoId: string;
    atividades: AtividadeDaMissaoPublica[];
  }) => ReactNode;
}

// O conteúdo da missão é **texto longo**: NUNCA é falado ao entrar na tela.
// No encontro há um aparelho por equipe, e meia dúzia deles lendo o conteúdo
// inteiro ao mesmo tempo é ruído, não acessibilidade — ele espera este
// controle (documento 15 §5.1, documento 03 §4). Só o conteúdo em texto o
// tem: imagem, vídeo, link e arquivo de apoio não têm o que ler em voz alta.
//
// A guarda é `disponivel`, não `ligada`: o controle **não depende** do liga e
// desliga das telas, porque quem o aciona está pedindo aquela leitura. E
// `disponivel` é `false` na camada inerte, que é o que mantém o controle fora
// da aplicação que ainda não monta o provedor (design — decisão 3).
function ControleDeOuvirOConteudo({ corpo }: { corpo: string }) {
  const { disponivel, ouvir } = useNarracao();
  if (!disponivel) return null;
  return (
    <Botao variante="secundaria" onClick={() => ouvir({ texto: corpo })}>
      Ouvir este texto
    </Botao>
  );
}

// Texto e link saem do próprio conteúdo. Imagem e vídeo vêm em bytes do
// núcleo, buscados por `MidiaDoNucleo` numa moldura de tamanho fixo: `<img
// src>` não manda a chave da aplicação que toda rota sob `/v1` exige
// (`RF-05-11`). Antes da fatia da moldura fixa, os três caíam em
// `conteudo.referencia` — a string do armazenamento impressa como se fosse
// o conteúdo, que não diz nada a quem lê.
function ConteudoDaMissao({
  conteudo,
  tituloDaMissao,
  token,
  aoMudarCarregamento,
}: {
  conteudo: MissaoPublica["conteudos"][number];
  tituloDaMissao: string;
  token: string | null;
  aoMudarCarregamento: (carregando: boolean) => void;
}) {
  const temArquivo = conteudo.referencia !== null;

  if (conteudo.tipo === "texto") return <>{conteudo.corpo}</>;
  if (conteudo.tipo === "link_externo") {
    return <a href={conteudo.endereco ?? "#"}>{conteudo.endereco}</a>;
  }

  // Envio não concluído não aparece quebrado: some da tela.
  if (!temArquivo) return null;

  if (conteudo.tipo === "imagem" || conteudo.tipo === "video") {
    return (
      <MidiaDoNucleo
        id={conteudo.id}
        buscar={lerArquivoDoConteudo}
        token={token}
        tipo={conteudo.tipo}
        alt={
          conteudo.tipo === "imagem"
            ? `Conteúdo de ${tituloDaMissao}`
            : `Vídeo de ${tituloDaMissao}`
        }
        textoDeErro="Esse arquivo não abriu agora. Tente de novo em instantes."
        aoMudarCarregamento={aoMudarCarregamento}
      />
    );
  }
  return <ArquivoDeApoio conteudoId={conteudo.id} token={token} />;
}

// O arquivo de apoio não é mídia embutida: é link para o Guerreiro(a) abrir
// o que o Mestre anexou.
function ArquivoDeApoio({ conteudoId, token }: { conteudoId: string; token: string | null }) {
  const [endereco, definirEndereco] = useState<string | null>(null);
  const [naoAbriu, definirNaoAbriu] = useState(false);

  useEffect(() => {
    if (!token) return;
    let local: string | null = null;
    let descartado = false;
    lerArquivoDoConteudo(conteudoId, token)
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
  }, [conteudoId, token]);

  if (naoAbriu) {
    return (
      <Aviso tipo="atencao">Esse arquivo não abriu agora. Tente de novo em instantes.</Aviso>
    );
  }
  if (!endereco) return <EstadoDaLista>Carregando o arquivo…</EstadoDaLista>;
  return <a href={endereco}>Abrir o arquivo de apoio</a>;
}

// O **ato** da missão: a sondagem, que abre a trilha ao ser respondida, ou o
// desafio de desbloqueio, que abre a missão seguinte. Um só dos dois, e
// nenhum deles enquanto o Mestre não julgar o prático já declarado
// (`RF-05-13`, `RF-05-14`, `RF-05-89`).
function AtoDaMissao({
  missao,
  aoDesbloquear,
  submissaoDoDesbloqueioLigada,
}: Pick<Props, "missao" | "aoDesbloquear" | "submissaoDoDesbloqueioLigada">) {
  if (!missao.e_proxima || missao.aguardando_mestre || !missao.desafio_de_desbloqueio) {
    return null;
  }
  return missao.e_sondagem ? (
    <Sondagem
      missaoId={missao.id}
      desafio={missao.desafio_de_desbloqueio}
      aoResponder={aoDesbloquear}
      submissaoLigada={submissaoDoDesbloqueioLigada}
    />
  ) : (
    <DesafioDeDesbloqueio
      missaoId={missao.id}
      desafio={missao.desafio_de_desbloqueio}
      aoDesbloquear={aoDesbloquear}
      submissaoLigada={submissaoDoDesbloqueioLigada}
    />
  );
}

// O conteúdo um por vez e, **depois do último deles**, o ato da missão. O
// ato ficava solto abaixo da sequência, visível desde o primeiro conteúdo:
// a criança via o quiz antes de ler o que a missão ensina, e responder sem
// percorrer o conteúdo transforma o corte de 60% em sorteio (`RN-05-45`,
// decisão do fundador de 2026-10-16). Missão **sem conteúdo algum** não tem
// o que percorrer e apresenta o ato de imediato — é o caso corrente da
// sondagem, que sem essa borda travaria a trilha inteira.
//
// Quem monta **tem de passar `key={missaoPublica.id}`**: é esta `key` que
// zera o índice quando a missão avança. Ela estava no `SequenciaPaginada` e
// desce para cá junto com o índice, porque a `Missao` NÃO remonta na troca
// de missão — índice guardado lá sobreviveria a ela, e a missão nova abriria
// no índice da anterior, com o ato liberado de cara (design — decisão 1).
//
// A posição é comandada de fora pelas propriedades que o paginador já
// oferece e que o quiz do desbloqueio já usa: `comum/react` não muda.
function ConteudoEAtoDaMissao({
  missao,
  missaoPublica,
  aoDesbloquear,
  submissaoDoDesbloqueioLigada,
}: Pick<Props, "missao" | "aoDesbloquear" | "submissaoDoDesbloqueioLigada"> & {
  missaoPublica: MissaoPublica;
}) {
  const { sessao } = useSessao();
  const token = sessao?.token ?? null;
  const [midiaCarregando, definirMidiaCarregando] = useState(false);
  const [indice, definirIndice] = useState(0);

  const conteudos = missaoPublica.conteudos.slice().sort((a, b) => a.ordem - b.ordem);
  // A sequência do conteúdo é de mão única — não há `rotuloDeVoltar` —, então
  // alcançar o último é monotônico: o ato aparece uma vez e não pisca.
  const alcancouOUltimo = conteudos.length === 0 || indice >= conteudos.length - 1;

  return (
    <>
      <SequenciaPaginada
        itens={conteudos}
        rotuloDeAvancar="Próximo conteúdo"
        indice={indice}
        aoIrPara={definirIndice}
        controlesTravados={midiaCarregando}
      >
        {(conteudo) => (
          <div className="cg-trilha__conteudo">
            <ConteudoDaMissao
              conteudo={conteudo}
              tituloDaMissao={missao.titulo}
              token={token}
              aoMudarCarregamento={definirMidiaCarregando}
            />
            {conteudo.autoria === "terceiro" && conteudo.fonte && (
              <span className="cg-trilha__credito"> — fonte: {conteudo.fonte}</span>
            )}
            {conteudo.tipo === "texto" && conteudo.corpo && (
              <ControleDeOuvirOConteudo corpo={conteudo.corpo} />
            )}
          </div>
        )}
      </SequenciaPaginada>

      {alcancouOUltimo && (
        <AtoDaMissao
          missao={missao}
          aoDesbloquear={aoDesbloquear}
          submissaoDoDesbloqueioLigada={submissaoDoDesbloqueioLigada}
        />
      )}
    </>
  );
}

// O conteúdo da missão e **o ato dela** — a sondagem, o desafio de
// desbloqueio ou a entrega da produção. É o primeiro grupo da tela, acima
// da primeira linha separadora: é o que a criança veio fazer (`RF-04-73`,
// `RF-05-11`, decisão do fundador de 2026-10-15).
//
// A **bibliografia** e o **crédito com a licença** NÃO moram aqui: são do
// `GuiaDaTrilha`, que os põe no grupo seguinte e no rodapé. O conteúdo sai
// **um por vez** (documento 15 §6.4), e a fonte do conteúdo de terceiro
// segue junto dele — é atribuição de autoria alheia. Missão bloqueada
// mostra o motivo direto, nunca recolhido nem cadeado mudo (`RF-05-10`).
export function Missao({
  missao,
  missaoPublica,
  erroDoConteudo = null,
  aoDesbloquear,
  submissaoDoDesbloqueioLigada,
  entregaDaProducao,
}: Props) {
  if (!missao.desbloqueada && !missao.e_proxima) {
    return (
      <Aviso tipo="atencao">
        Essa missão ainda está trancada. {missao.motivo_do_bloqueio}
      </Aviso>
    );
  }

  return (
    <article aria-label={missao.titulo} className="cg-trilha__missao">
      <h2>{missao.titulo}</h2>
      {missao.obrigatoria === false && (
        <Aviso tipo="andamento">
          Essa missão é opcional — ela não conta no que falta para o próximo nível.
        </Aviso>
      )}

      {erroDoConteudo && <Aviso tipo="erro">{erroDoConteudo}</Aviso>}
      {!erroDoConteudo && missaoPublica === undefined && (
        <EstadoDaLista>Carregando o conteúdo da missão…</EstadoDaLista>
      )}

      {missaoPublica ? (
        <ConteudoEAtoDaMissao
          key={missaoPublica.id}
          missao={missao}
          missaoPublica={missaoPublica}
          aoDesbloquear={aoDesbloquear}
          submissaoDoDesbloqueioLigada={submissaoDoDesbloqueioLigada}
        />
      ) : (
        // Conteúdo que **falhou** não prende a missão: o gate existe para
        // garantir o percurso, e o que não pode ser servido não tem o que
        // guardar — fechado, deixaria a criança sem saída, porque o ato é o
        // caminho adiante. Enquanto **carrega** segue oculto, para não
        // aparecer e sumir quando a lista chegar (decisão do fundador de
        // 2026-10-16).
        erroDoConteudo && (
          <AtoDaMissao
            missao={missao}
            aoDesbloquear={aoDesbloquear}
            submissaoDoDesbloqueioLigada={submissaoDoDesbloqueioLigada}
          />
        )
      )}

      {missao.aguardando_mestre && (
        <Aviso tipo="andamento">
          Você declarou que cumpriu! Agora é só esperar o Mestre conferir.
        </Aviso>
      )}

      {missao.desbloqueada &&
        missaoPublica &&
        entregaDaProducao?.({ missaoId: missao.id, atividades: missaoPublica.atividades })}
    </article>
  );
}

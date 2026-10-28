import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, MarcaDeGravacao } from "comum/react";
import { useState } from "react";
import {
  type ConteudoDaMissao,
  type DirecaoDoMovimento,
  type MissaoDaTrilha,
  moverConteudo,
  removerConteudo,
  type TipoDeConteudo,
} from "./api";
import { ConteudoExibido } from "./ConteudoExibido";
import { FormularioDeConteudo } from "./FormularioDeConteudo";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

const ROTULO_DO_TIPO: Record<TipoDeConteudo, string> = {
  texto: "Texto",
  imagem: "Imagem",
  link_externo: "Link externo",
  video: "Vídeo",
  arquivo: "Arquivo de apoio",
};

// Os três tipos que guardam bytes: são eles que só buscam o arquivo quando o
// Mestre pede a exibição (`RN-09-46`).
const TIPOS_COM_ARQUIVO: TipoDeConteudo[] = ["imagem", "video", "arquivo"];

const LIMITE_DO_RESUMO = 60;

function formatarMb(tamanho: number): string {
  return `${(tamanho / (1024 * 1024)).toFixed(1)} MB`;
}

// O rótulo distingue um conteúdo do outro na lista. Antes, a linha imprimia o
// valor cru do tipo, e três conteúdos de texto na mesma missão apareciam como
// três linhas iguais dizendo "texto" — não havia como escolher qual corrigir
// (`RF-09-125`).
//
// Nos tipos com envio o rótulo sai do **tipo e do tamanho**, não do nome do
// arquivo: o núcleo nunca guardou o nome, só a referência derivada do id do
// conteúdo, e inventar uma coluna para ele seria decisão de produto que
// ninguém tomou.
export function rotuloDoConteudo(conteudo: ConteudoDaMissao): string {
  if (conteudo.tipo === "texto") {
    const corpo = (conteudo.corpo ?? "").trim();
    if (!corpo) return "Texto sem corpo";
    return corpo.length > LIMITE_DO_RESUMO ? `${corpo.slice(0, LIMITE_DO_RESUMO)}…` : corpo;
  }
  if (conteudo.tipo === "link_externo") {
    const endereco = (conteudo.endereco ?? "").trim();
    if (!endereco) return "Link sem endereço";
    try {
      return new URL(endereco).hostname;
    } catch {
      // Endereço que o navegador não sabe analisar segue legível como está:
      // a tela nunca esconde o que está gravado.
      return endereco;
    }
  }
  const nome = ROTULO_DO_TIPO[conteudo.tipo];
  if (conteudo.referencia === null) return `${nome} — envio pendente`;
  return conteudo.tamanho === null ? nome : `${nome} — ${formatarMb(conteudo.tamanho)}`;
}

// O rótulo do texto **é** o começo do corpo: quando o corpo inteiro cabe
// nele, exibi-lo embaixo imprimiria o mesmo parágrafo duas vezes. Exibe-se o
// texto quando há mais para ver do que o rótulo já mostra (`RF-09-125`).
function oRotuloJaMostraTudo(conteudo: ConteudoDaMissao): boolean {
  return conteudo.tipo === "texto" && (conteudo.corpo ?? "").trim().length <= LIMITE_DO_RESUMO;
}

function rotuloDaAutoria(conteudo: ConteudoDaMissao): string {
  return conteudo.autoria === "terceiro"
    ? `De terceiro — fonte: ${conteudo.fonte ?? "não declarada"}`
    : "Autoria própria";
}

// O bloco Conteúdo do cadastro: lista, identifica, exibe, corrige, remove e
// ordena. Exibir é **sob demanda** nos tipos com arquivo, porque
// `BlocoRecolhivel` monta os filhos mesmo fechado e `MidiaDoNucleo` busca os
// bytes na montagem — exibir tudo de saída faria abrir a tela da trilha puxar
// os arquivos de todas as missões da etapa pelo núcleo (`RF-09-125`,
// `RN-09-46`, design — decisão 7).
export function BlocoDeConteudo({ missao, onAtualizada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [criando, definirCriando] = useState(false);
  const [emCorrecao, definirEmCorrecao] = useState<string | null>(null);
  const [exibindo, definirExibindo] = useState<Record<string, boolean>>({});
  const [erro, definirErro] = useState<Record<string, string>>({});
  const [gravadoEm, definirGravadoEm] = useState<Date | null>(null);

  const conteudos = [...(missao.conteudos ?? [])].sort((a, b) => a.ordem - b.ordem);

  function recusaDoNucleo(erroCapturado: unknown, alternativa: string): string | null {
    if (ehRecusaDeSessao(erroCapturado)) {
      tratarRecusaDeSessao();
      return null;
    }
    return erroCapturado instanceof ErroDaApi ? erroCapturado.message : alternativa;
  }

  function semOConteudo<T>(mapa: Record<string, T>, id: string): Record<string, T> {
    const { [id]: _removido, ...resto } = mapa;
    return resto;
  }

  async function remover(conteudo: ConteudoDaMissao) {
    if (!sessao) return;
    definirErro((atual) => semOConteudo(atual, conteudo.id));
    try {
      await removerConteudo(conteudo.id, sessao.token);
    } catch (erroCapturado) {
      const recusa = recusaDoNucleo(
        erroCapturado,
        "Não foi possível remover este conteúdo. Tente novamente em instantes.",
      );
      if (recusa) definirErro((atual) => ({ ...atual, [conteudo.id]: recusa }));
      return;
    }
    definirExibindo((atual) => semOConteudo(atual, conteudo.id));
    definirGravadoEm(new Date());
    onAtualizada({
      ...missao,
      conteudos: conteudos.filter((outro) => outro.id !== conteudo.id),
    });
  }

  async function mover(conteudo: ConteudoDaMissao, direcao: DirecaoDoMovimento) {
    if (!sessao) return;
    definirErro((atual) => semOConteudo(atual, conteudo.id));
    let movido: ConteudoDaMissao;
    try {
      movido = await moverConteudo(conteudo.id, direcao, sessao.token);
    } catch (erroCapturado) {
      const recusa = recusaDoNucleo(
        erroCapturado,
        "Não foi possível mover este conteúdo. Tente novamente em instantes.",
      );
      if (recusa) definirErro((atual) => ({ ...atual, [conteudo.id]: recusa }));
      return;
    }
    // A troca é de duas ordens, e o núcleo devolve só o conteúdo movido: o
    // vizinho recebe de volta a ordem que o movido tinha.
    const ordemAnterior = conteudo.ordem;
    definirGravadoEm(new Date());
    onAtualizada({
      ...missao,
      conteudos: conteudos.map((outro) => {
        if (outro.id === movido.id) return movido;
        return outro.ordem === movido.ordem ? { ...outro, ordem: ordemAnterior } : outro;
      }),
    });
  }

  function aoCorrigido(corrigido: ConteudoDaMissao) {
    definirEmCorrecao(null);
    definirGravadoEm(new Date());
    onAtualizada({
      ...missao,
      conteudos: conteudos.map((outro) => (outro.id === corrigido.id ? corrigido : outro)),
    });
  }

  return (
    <section aria-label={`Conteúdo de ${missao.titulo}`}>
      <ul>
        {conteudos.map((conteudo, posicao) => (
          <li key={conteudo.id}>
            {emCorrecao === conteudo.id ? (
              <FormularioDeConteudo
                idDaMissao={missao.id}
                conteudo={conteudo}
                onSalvo={aoCorrigido}
                onCancelar={() => definirEmCorrecao(null)}
              />
            ) : (
              <>
                <p>{rotuloDoConteudo(conteudo)}</p>
                <p>{rotuloDaAutoria(conteudo)}</p>

                {!TIPOS_COM_ARQUIVO.includes(conteudo.tipo) &&
                  !oRotuloJaMostraTudo(conteudo) && (
                    <ConteudoExibido conteudo={conteudo} tituloDaMissao={missao.titulo} />
                  )}
                {TIPOS_COM_ARQUIVO.includes(conteudo.tipo) &&
                  (exibindo[conteudo.id] ? (
                    <ConteudoExibido conteudo={conteudo} tituloDaMissao={missao.titulo} />
                  ) : (
                    <Botao
                      variante="secundaria"
                      onClick={() =>
                        definirExibindo((atual) => ({ ...atual, [conteudo.id]: true }))
                      }
                    >
                      Exibir {ROTULO_DO_TIPO[conteudo.tipo].toLowerCase()}
                    </Botao>
                  ))}

                <Botao variante="secundaria" onClick={() => definirEmCorrecao(conteudo.id)}>
                  Corrigir
                </Botao>
                <Botao variante="secundaria" onClick={() => remover(conteudo)}>
                  Remover
                </Botao>
                <Botao
                  variante="secundaria"
                  desabilitado={posicao === 0}
                  onClick={() => mover(conteudo, "cima")}
                >
                  Subir
                </Botao>
                <Botao
                  variante="secundaria"
                  desabilitado={posicao === conteudos.length - 1}
                  onClick={() => mover(conteudo, "baixo")}
                >
                  Descer
                </Botao>
                {erro[conteudo.id] && <Aviso tipo="erro">{erro[conteudo.id]}</Aviso>}
              </>
            )}
          </li>
        ))}
      </ul>

      {criando ? (
        <FormularioDeConteudo
          idDaMissao={missao.id}
          onSalvo={(conteudo) => {
            definirCriando(false);
            definirGravadoEm(new Date());
            onAtualizada({ ...missao, conteudos: [...conteudos, conteudo] });
          }}
          onCancelar={() => definirCriando(false)}
        />
      ) : (
        <Botao variante="secundaria" onClick={() => definirCriando(true)}>
          Novo conteúdo
        </Botao>
      )}
      <MarcaDeGravacao instante={gravadoEm} />
    </section>
  );
}

import type { ReactNode } from "react";
import { CAMINHO_DO_CONVITE } from "../navegacao/caminhos";

/**
 * O herói da abertura: a ilustração do elenco em primeiro plano, a frase que
 * diz o que o projeto é, e as ações que a vitrine já oferece (`RF-03-01`,
 * `RF-03-51`, `RF-03-58`).
 *
 * O documento 15 §6 dá à Arena **ilustração em primeiro plano**, e sem ela a
 * abertura caía direto na navegação de recortes — onze seções com o mesmo
 * peso, e uma lista como primeira coisa a ler.
 *
 * **Sem diretiva de cliente**, de propósito: não tem estado e não busca nada,
 * então sai no documento servido e não custa JS. É também o que permite à
 * composição de teste montar **este mesmo componente**, em vez de espelhar a
 * marcação à mão como `NavegacaoDeRecortes.astro` obriga.
 *
 * **O "Entrar" é do herói, e é um só na tela.** A página o passa como filho —
 * `EntradaDaAbertura`, que é ilha porque o diálogo tem estado —, e
 * `Vitrine.astro` diz ao cabeçalho para não trazer o dele. Até 2026-10-09 o
 * botão morava só no cabeçalho; a decisão do fundador de 2026-10-10 o traz
 * para junto do "Quero apoiar", **sem duplicá-lo**.
 *
 * "Quero apoiar" é **link**, não botão: trocar de tela é trocar de
 * documento desde a fatia 9, e um `<a>` navega sem JS nenhum.
 */

/** Os quatro do documento 15 §13.6, **na ordem da composição**: os dois
 * estudantes nas extremidades e, ao centro, o professor ao lado da criatura que
 * a mão dele indica. A ordem não é livre — Trenell precisa ficar vizinho ao
 * Robô Educa, senão o gesto dele aponta para o vazio (decisão do fundador de
 * 2026-10-10).
 *
 * A largura e a altura são as do arquivo, declaradas para a tela não pular
 * quando a ilustração chega (documento 15 §1, princípio 4). */
const ELENCO = [
  { arquivo: "susy", largura: 578 },
  { arquivo: "robo-educa", largura: 764 },
  { arquivo: "trenell", largura: 551 },
  { arquivo: "otavio", largura: 361 },
] as const;

const ALTURA = 1024;

/** A frase é a do documento 01 §1 — a definição do projeto, não uma redação
 * nova. */
const FRASE =
  "Plataforma educacional gamificada, de código aberto, que conecta jovens, " +
  "mestres e apoiadores para promover educação, tecnologia e cidadania em " +
  "comunidades periféricas.";

interface Props {
  /** O "Entrar" do par, montado pela página porque tem estado — o diálogo — e
   * o herói não. Ausente, o herói apresenta só "Quero apoiar". */
  children?: ReactNode;
}

export function Heroi({ children }: Props) {
  return (
    <section className="cg-heroi" aria-label="O que é o Comunidade Game">
      {/* Um rótulo só para as quatro figuras, e não um por imagem: quem usa
          leitor de tela ouve o elenco uma vez, em vez de quatro nomes soltos.
          As imagens ficam com `alt` vazio porque o rótulo do grupo já diz o
          que elas são. */}
      <div
        className="cg-heroi__elenco"
        role="img"
        aria-label="Susy, o Robô Educa, o professor Carlos Trenell e Otávio, o elenco do Comunidade Game"
      >
        {ELENCO.map(({ arquivo, largura }) => (
          <picture key={arquivo}>
            <source srcSet={`/elenco/${arquivo}.avif`} type="image/avif" />
            <img
              src={`/elenco/${arquivo}.webp`}
              alt=""
              width={largura}
              height={ALTURA}
              // Fora do caminho crítico: a frase e a ação abaixo são texto e
              // link, e continuam de pé sem a ilustração.
              loading="lazy"
              decoding="async"
            />
          </picture>
        ))}
      </div>
      <p className="cg-heroi__frase">{FRASE}</p>
      {/* As duas ações lado a lado, como **par de iguais**: mesma altura,
          mesma forma e mesmo peso, distinguidas por cor e por rótulo. A cor
          não é sinal único — cada botão diz o que faz (documento 15 §5). */}
      <div className="cg-heroi__acoes">
        <a className="cg-botao cg-botao--primaria cg-heroi__acao" href={CAMINHO_DO_CONVITE}>
          Quero apoiar
        </a>
        {children}
      </div>
    </section>
  );
}

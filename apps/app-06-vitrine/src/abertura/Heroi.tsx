import { CAMINHO_DO_CONVITE } from "../navegacao/caminhos";

/**
 * O herói da abertura: a ilustração do elenco em primeiro plano, a frase que
 * diz o que o projeto é, e a ação que a vitrine já oferece (`RF-03-01`,
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
 * **"Entrar" não se repete aqui.** Ele é do cabeçalho, que fica logo acima e o
 * põe em toda tela pública (`RF-03-58`); um segundo botão de mesmo nome na
 * mesma tela não acrescenta ação nenhuma e atrapalha quem navega por leitor de
 * tela. Decisão do fundador de 2026-10-09.
 *
 * "Quero participar" é **link**, não botão: trocar de tela é trocar de
 * documento desde a fatia 9, e um `<a>` navega sem JS nenhum.
 */

/** Os quatro do documento 15 §13.6, na ordem em que aparecem. A largura e a
 * altura são as do arquivo, declaradas para a tela não pular quando a
 * ilustração chega (documento 15 §1, princípio 4). */
const ELENCO = [
  { arquivo: "susy", largura: 570 },
  { arquivo: "otavio", largura: 401 },
  { arquivo: "trenell", largura: 551 },
  { arquivo: "robo-educa", largura: 764 },
] as const;

const ALTURA = 1024;

/** A frase é a do documento 01 §1 — a definição do projeto, não uma redação
 * nova. */
const FRASE =
  "Plataforma educacional gamificada, de código aberto, que conecta jovens, " +
  "mestres e apoiadores para promover educação, tecnologia e cidadania em " +
  "comunidades periféricas.";

export function Heroi() {
  return (
    <section className="cg-heroi" aria-label="O que é o Comunidade Game">
      {/* Um rótulo só para as quatro figuras, e não um por imagem: quem usa
          leitor de tela ouve o elenco uma vez, em vez de quatro nomes soltos.
          As imagens ficam com `alt` vazio porque o rótulo do grupo já diz o
          que elas são. */}
      <div
        className="cg-heroi__elenco"
        role="img"
        aria-label="Susy, Otávio, o professor Carlos Trenell e o Robô Educa, o elenco do Comunidade Game"
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
      <a className="cg-botao cg-botao--primaria cg-heroi__acao" href={CAMINHO_DO_CONVITE}>
        Quero participar
      </a>
    </section>
  );
}

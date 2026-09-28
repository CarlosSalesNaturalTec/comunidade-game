// A **representação visual da Comunidade Virtual** do documento 11 §8.3: o
// território "ganha corpo" na medida do dado real, e nunca por decoração
// (documento 15 §5).
//
// Toda medida do desenho é **razão entre contagens publicadas** — nenhuma
// constante de estilo decide o tamanho de nada:
//
// | O que acontece no motor         | O que muda no desenho                    |
// | ------------------------------- | ---------------------------------------- |
// | Comunidade criada, sem registro | Só o contorno e o nome                   |
// | Bairro publicado a mais         | Um lado a mais no contorno               |
// | Tipo de coleta ativo            | Um anel próprio, nomeado                 |
// | Registros acumulados no tipo    | O anel daquele tipo cresce               |
// | Série interrompida              | O anel permanece, tracejado e rotulado   |
//
// A forma é **a mesma para todo tipo de coleta**: termômetro, pluviômetro e
// mapa de vias exigiriam um campo de forma no catálogo de tipos, que nenhum
// documento define (decisão do fundador de 2026-09-28).
//
// O desenho **nunca é a única via ao conteúdo** (documento 15 §5): ele é
// `role="img"` com rótulo em texto, e a mesma informação sai na lista abaixo
// dele, legível sem depender de cor nem de imagem.

export interface CamadaDoTerritorio {
  /** O nome do tipo de coleta, como o catálogo o cadastrou. */
  tipo: string;
  /** Registros válidos publicados daquele tipo, no recorte consultado. */
  registrosValidos: number;
  /** `false` quando nenhuma série que compõe o recorte está ativa. */
  ativo: boolean;
}

interface Props {
  nome: string;
  /** Bairros que aparecem no recorte publicado — o **detalhe** do contorno.
   * Zero desenha o contorno mínimo. */
  bairrosPublicados?: number;
  camadas?: CamadaDoTerritorio[];
  /** Os quatro indicadores chegam nulos na comunidade abaixo do piso: o
   * contorno sai sem preenchimento, como no território vazio. */
  seriesAbertas?: number | null;
  seriesAtivas?: number | null;
}

const LADOS_MINIMOS = 3;
const RAIO = 48;
const CENTRO = 50;

/** Polígono regular de `lados` lados — um lado por bairro publicado, com o
 * triângulo como piso: abaixo de três não há polígono. */
function contorno(lados: number): string {
  const total = Math.max(LADOS_MINIMOS, lados);
  return Array.from({ length: total }, (_, indice) => {
    const angulo = (2 * Math.PI * indice) / total - Math.PI / 2;
    const x = CENTRO + RAIO * Math.cos(angulo);
    const y = CENTRO + RAIO * Math.sin(angulo);
    return `${x.toFixed(2)},${y.toFixed(2)}`;
  }).join(" ");
}

export function TerritorioDaComunidade({
  nome,
  bairrosPublicados = 0,
  camadas = [],
  seriesAbertas = null,
  seriesAtivas = null,
}: Props) {
  const totalDeRegistros = camadas.reduce((soma, camada) => soma + camada.registrosValidos, 0);
  const vazio = totalDeRegistros === 0;
  // A vitalidade do contorno é a fração das séries que seguem ativas — razão
  // entre dois números que a própria leitura devolve.
  const vitalidade =
    seriesAbertas && seriesAtivas !== null && seriesAbertas > 0
      ? seriesAtivas / seriesAbertas
      : 0;

  const aneis = camadas.map((camada) => ({
    ...camada,
    // A participação do tipo nos registros válidos publicados da comunidade.
    raio: (RAIO * camada.registrosValidos) / (totalDeRegistros || 1),
  }));

  const descricao = vazio
    ? `Território de ${nome}, ainda vazio`
    : `Território de ${nome}, com ${camadas.length} tipo(s) de coleta e ` +
      `${bairrosPublicados} bairro(s) publicado(s)`;

  return (
    <div className="cg-territorio">
      <svg
        className="cg-territorio__desenho"
        viewBox="0 0 100 100"
        role="img"
        aria-label={descricao}
        data-vazio={vazio ? "sim" : "nao"}
      >
        <polygon
          className="cg-territorio__contorno"
          points={contorno(bairrosPublicados)}
          fillOpacity={vitalidade}
        />
        {aneis.map((anel) => (
          <circle
            key={anel.tipo}
            className="cg-territorio__camada"
            cx={CENTRO}
            cy={CENTRO}
            r={anel.raio}
            data-ativo={anel.ativo ? "sim" : "nao"}
            strokeDasharray={anel.ativo ? undefined : "3 2"}
          />
        ))}
      </svg>
      {vazio ? (
        <p className="cg-territorio__vazio">
          Território ainda vazio — nenhum registro publicado.
        </p>
      ) : (
        <ul className="cg-territorio__legenda">
          {camadas.map((camada) => (
            <li key={camada.tipo}>
              {camada.tipo}: {camada.registrosValidos} registro(s) válido(s)
              {camada.ativo ? "" : " — série inativa"}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

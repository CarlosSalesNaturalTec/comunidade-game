import { CAMINHO_DA_AREA_DETALHADA } from "../navegacao/caminhos";

// Aviso discreto, em toda tela da vitrine: não bloqueia, não pede
// confirmação e não guarda nada no aparelho — nem que foi visto ou acionado
// (`RN-03-23`, `RF-03-51`, documento 03 §12).
export function AvisoDeColeta({ irPara }: { irPara: (destino: string) => void }) {
  return (
    <aside className="cg-aviso-de-coleta" aria-label="Aviso de coleta de dados">
      <p>
        Esta vitrine não coleta dado de quem visita. Só os formulários guardam o que você
        digita.{" "}
        <button
          type="button"
          className="cg-aviso-de-coleta__botao"
          onClick={() => irPara(CAMINHO_DA_AREA_DETALHADA)}
        >
          Saiba o que a plataforma coleta
        </button>
      </p>
    </aside>
  );
}

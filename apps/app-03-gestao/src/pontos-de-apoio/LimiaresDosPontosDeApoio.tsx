import { Aviso, BlocoRecolhivel, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { type LimiarDoPontoDeApoio, listarLimiaresDosPontosDeApoio } from "./api";

interface Props {
  token: string;
}

function formatarMomento(iso: string): string {
  return new Date(iso).toLocaleString("pt-BR");
}

function faixa(distancias: number[]): string {
  if (distancias.length === 0) return "—";
  return `${Math.min(...distancias).toFixed(3)} a ${Math.max(...distancias).toFixed(3)}`;
}

// O limiar de comparação vigente de cada ponto de apoio, com a origem da
// medição que o produziu, e o destaque de quem ainda não tem (`RF-02-109`).
//
// **Consulta apenas.** Não existe caminho de edição aqui: o número nasce de
// uma medição no aparelho do encontro, e permitir digitá-lo desfaria a
// garantia de que todo limiar vigente foi medido (`RF-04-66`).
export function LimiaresDosPontosDeApoio({ token }: Props) {
  const [limiares, definirLimiares] = useState<LimiarDoPontoDeApoio[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    listarLimiaresDosPontosDeApoio(token)
      .then(definirLimiares)
      .catch(() => {
        definirErro("Não foi possível carregar os limiares. Tente novamente em instantes.");
      });
  }, [token]);

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (limiares === null) return <EstadoDaLista>Carregando os limiares…</EstadoDaLista>;

  const semMedicao = limiares.filter((linha) => linha.medicao === null);

  return (
    <section className="cg-limiares">
      <h3>Reconhecimento facial por ponto de apoio</h3>

      {semMedicao.length > 0 && (
        <Aviso tipo="atencao">
          {semMedicao.length === 1
            ? "Um ponto de apoio ainda não teve o limiar medido"
            : `${semMedicao.length} pontos de apoio ainda não tiveram o limiar medido`}
          : {semMedicao.map((linha) => linha.nome).join(", ")}. Ali o reconhecimento facial não
          confere ninguém, e todo Guerreiro(a) entra pela confirmação de Mestre ou Admin. A
          medição é feita no aparelho do encontro, pela App 01.
        </Aviso>
      )}

      {limiares.length === 0 ? (
        <EstadoDaLista>Nenhum espaço cadastrado para calibrar.</EstadoDaLista>
      ) : (
        <ul className="cg-limiares-lista">
          {limiares.map((linha) => (
            <li key={linha.ponto_de_apoio_id}>
              <strong>{linha.nome}</strong>{" "}
              {linha.medicao === null ? (
                <span className="cg-limiar-ausente">sem limiar medido</span>
              ) : (
                <>
                  <span>limiar {linha.medicao.limiar.toFixed(3)}</span>
                  <BlocoRecolhivel
                    titulo="Como este número foi medido"
                    resumo={`${linha.medicao.distancias_do_piso.length} capturas de piso, ${linha.medicao.distancias_do_teto.length} de teto`}
                  >
                    <p>Medido em {formatarMomento(linha.medicao.registrado_em)}.</p>
                    <p>
                      Piso — mesma pessoa, {linha.medicao.distancias_do_piso.length} capturas:{" "}
                      {faixa(linha.medicao.distancias_do_piso)}
                    </p>
                    <p>
                      Teto — {linha.medicao.pessoas_no_teto} pessoas,{" "}
                      {linha.medicao.distancias_do_teto.length} capturas:{" "}
                      {faixa(linha.medicao.distancias_do_teto)}
                    </p>
                  </BlocoRecolhivel>
                </>
              )}
            </li>
          ))}
        </ul>
      )}

      <p className="cg-limiares-nota">
        O limiar não se edita aqui: ele nasce de uma medição no aparelho do encontro. Para
        corrigi-lo, meça de novo pela App 01.
      </p>
    </section>
  );
}

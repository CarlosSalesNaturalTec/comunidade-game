import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import { declararCadenciaDeRetomada, type MissaoDaTrilha } from "./api";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

function analisarDias(texto: string): number[] {
  return texto
    .split(",")
    .map((parte) => Number(parte.trim()))
    .filter((numero) => Number.isInteger(numero) && numero > 0);
}

// A cadência é sempre a que o Mestre declara — a sugestão de 2, 7 e 21 dias
// é do _template_ de missão, que não é desta fatia (`RF-09-83`, `RF-09-101`).
export function CadenciaDeRetomada({ missao, onAtualizada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [dias, definirDias] = useState(missao.cadencia_de_retomada?.join(", ") ?? "");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function declarar() {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      const atualizada = await declararCadenciaDeRetomada(
        missao.id,
        analisarDias(dias),
        sessao.token,
      );
      onAtualizada(atualizada);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível declarar a cadência. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  async function deixarSemRetomada() {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      const atualizada = await declararCadenciaDeRetomada(missao.id, null, sessao.token);
      definirDias("");
      onAtualizada(atualizada);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível declarar a cadência. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="cadencia-de-retomada">
      <Campo
        rotulo="Cadência de retomada (dias do desbloqueio, separados por vírgula)"
        valor={dias}
        aoAlterar={definirDias}
      />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao variante="secundaria" onClick={declarar} desabilitado={enviando}>
        Declarar cadência
      </Botao>
      <Botao variante="secundaria" onClick={deixarSemRetomada} desabilitado={enviando}>
        Deixar sem retomada
      </Botao>
    </div>
  );
}

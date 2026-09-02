import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type ChangeEvent, type FormEvent, useState } from "react";
import { declararAporte } from "../aportes/api";
import { formatarMoedas, REAIS_POR_MOEDA } from "../compartilhado/escada";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { MissaoDoApoiador } from "./api";

const FORMATOS_ACEITOS = "PDF, JPG ou PNG";

interface Props {
  missao: MissaoDoApoiador;
  aoVoltar: () => void;
}

// Cobrir a missão escolhida, inteira ou em parte, sempre com comprovante —
// e a declaração de que ela entra pendente, sem abater o que falta nem
// concluir a missão até a homologação (`RF-14-63`, `RF-14-64`, `RN-14-32`).
export function DeclaracaoPorMissao({ missao, aoVoltar }: Props) {
  const { sessao } = useSessao();
  const valorSugeridoEmReais = Number(missao.falta) * REAIS_POR_MOEDA;
  const [valorEmReaisTexto, definirValorEmReaisTexto] = useState(
    valorSugeridoEmReais.toFixed(2),
  );
  const [comprovante, definirComprovante] = useState<File | null>(null);

  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  const valorEmReais = Number(valorEmReaisTexto.replace(",", "."));
  const valorValido =
    valorEmReaisTexto.trim() !== "" && !Number.isNaN(valorEmReais) && valorEmReais > 0;

  function aoEscolherComprovante(evento: ChangeEvent<HTMLInputElement>) {
    definirComprovante(evento.target.files?.[0] ?? null);
  }

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    definirErro(null);
    definirSucesso(false);

    if (!sessao) return;
    if (!valorValido) {
      definirErro("Informe um valor válido.");
      return;
    }
    if (!comprovante) {
      definirErro(`Anexe o comprovante em ${FORMATOS_ACEITOS} para enviar a declaração.`);
      return;
    }

    definirEnviando(true);
    try {
      await declararAporte(
        {
          valor_declarado: valorEmReais,
          origem_da_escolha: "missao",
          missao_do_apoiador_id: missao.id,
          comprovante,
        },
        sessao.token,
      );
      definirSucesso(true);
      definirComprovante(null);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível enviar a declaração. Tente novamente.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo={`Cobrir: ${missao.titulo}`}
        subtitulo={missao.o_que_se_pede}
        acao={{ rotulo: "Voltar às missões", aoAcionar: aoVoltar }}
      />

      <AvisoDeColeta dado="o valor declarado e o comprovante da cobertura da missão" />

      <p>
        Falta {missao.falta} moedas para fechar esta missão — o selo é "{missao.selo_nome}".
      </p>

      <form onSubmit={aoEnviar}>
        <Campo
          rotulo="Valor a cobrir (R$)"
          tipo="number"
          valor={valorEmReaisTexto}
          aoAlterar={definirValorEmReaisTexto}
        />
        {valorValido && <p>Equivalente a {formatarMoedas(valorEmReais)}.</p>}
        <p>
          Você pode cobrir a missão inteira ou só parte dela: o restante continua aberto para
          outras pessoas.
        </p>

        <div className="cg-campo">
          <label htmlFor="comprovante-da-missao">
            Comprovante da transferência ({FORMATOS_ACEITOS})
          </label>
          <input id="comprovante-da-missao" type="file" onChange={aoEscolherComprovante} />
        </div>

        <p>
          O aporte entra <strong>pendente de homologação</strong> e não abate o que falta nem
          conclui a missão. Só quando um Admin homologar é que ele abate o que falta e,
          fechando o saldo, conclui a missão e credita o selo.
        </p>

        <Botao tipo="submit" desabilitado={enviando}>
          Enviar declaração
        </Botao>
      </form>

      {enviando && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {sucesso && (
        <Aviso tipo="sucesso">
          Declaração registrada na fila da gestão. A missão continua aberta com o mesmo quanto
          falta até a homologação.
        </Aviso>
      )}
    </Moldura>
  );
}

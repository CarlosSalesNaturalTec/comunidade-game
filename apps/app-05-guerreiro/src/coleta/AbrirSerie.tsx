import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useEffect, useId, useState } from "react";
import {
  abrirSerie,
  type DesafioDisponivel,
  type Local,
  listarDesafiosDisponiveis,
  listarLocaisDaComunidade,
} from "../api/coleta";

// A recusa da abertura é sempre explicada nesta frase única, em vez do
// texto técnico que o núcleo devolve — o núcleo continua sendo a
// autoridade, a tela só traduz (`RF-05-31`, `RN-05-11`, `RN-05-24`, design
// — Risks).
const RECUSA_DA_ABERTURA =
  "Não foi possível abrir essa série agora. Escolha outro desafio ou local e tente de novo.";

interface Props {
  aoAbrir: () => void;
  aoSolicitarLocalFaltante: (contexto: {
    desafioId: string;
    comunidadeId: string;
    nivel: string;
  }) => void;
}

// Abertura de série: escolha do desafio entre os disponíveis e do local
// entre os cadastrados do nível exigido — a aplicação nunca cadastra local
// (`RF-05-31`, PRD-05 §§3.2, 5.4).
export function AbrirSerie({ aoAbrir, aoSolicitarLocalFaltante }: Props) {
  const { sessao } = useSessao();
  const idDoCampo = useId();
  const [desafios, definirDesafios] = useState<DesafioDisponivel[] | null>(null);
  const [locais, definirLocais] = useState<Local[]>([]);
  const [desafioId, definirDesafioId] = useState("");
  const [localId, definirLocalId] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarDesafiosDisponiveis(sessao.token)
      .then((pagina) =>
        definirDesafios(pagina.itens.filter((desafio) => !desafio.ja_assumido)),
      )
      .catch(() => definirDesafios([]));
  }, [sessao]);

  const desafioEscolhido = desafios?.find((desafio) => desafio.id === desafioId) ?? null;

  useEffect(() => {
    definirLocalId("");
    if (!desafioEscolhido) {
      definirLocais([]);
      return;
    }
    listarLocaisDaComunidade(desafioEscolhido.comunidade_virtual_id)
      .then((pagina) =>
        definirLocais(
          pagina.itens.filter(
            (local) => local.nivel === desafioEscolhido.granularidade_exigida,
          ),
        ),
      )
      .catch(() => definirLocais([]));
  }, [desafioEscolhido]);

  async function aoEnviar() {
    if (!sessao || !desafioEscolhido || !localId) return;
    definirEnviando(true);
    definirErro(null);
    try {
      await abrirSerie({ desafioDeColetaId: desafioEscolhido.id, localId }, sessao.token);
      aoAbrir();
    } catch {
      definirErro(RECUSA_DA_ABERTURA);
    } finally {
      definirEnviando(false);
    }
  }

  if (desafios === null) {
    return <EstadoDaLista>Carregando os desafios disponíveis…</EstadoDaLista>;
  }

  if (desafios.length === 0) {
    return <EstadoDaLista>Não há nenhum desafio de coleta disponível agora.</EstadoDaLista>;
  }

  return (
    <section aria-label="Abrir série de coleta">
      <div className="cg-campo">
        <label htmlFor={`${idDoCampo}-desafio`}>Qual desafio você quer assumir?</label>
        <select
          id={`${idDoCampo}-desafio`}
          value={desafioId}
          onChange={(evento) => definirDesafioId(evento.target.value)}
        >
          <option value="">Escolha um desafio</option>
          {desafios.map((desafio) => (
            <option key={desafio.id} value={desafio.id}>
              {desafio.tipo_de_coleta.nome}
            </option>
          ))}
        </select>
      </div>

      {desafioEscolhido && (
        <div className="cg-campo">
          <label htmlFor={`${idDoCampo}-local`}>Em qual local?</label>
          {locais.length === 0 ? (
            <>
              <p>Nenhum local desse tipo está cadastrado ainda.</p>
              <Botao
                variante="secundaria"
                onClick={() =>
                  aoSolicitarLocalFaltante({
                    desafioId: desafioEscolhido.id,
                    comunidadeId: desafioEscolhido.comunidade_virtual_id,
                    nivel: desafioEscolhido.granularidade_exigida,
                  })
                }
              >
                Pedir para incluir o local
              </Botao>
            </>
          ) : (
            <select
              id={`${idDoCampo}-local`}
              value={localId}
              onChange={(evento) => definirLocalId(evento.target.value)}
            >
              <option value="">Escolha um local</option>
              {locais.map((local) => (
                <option key={local.id} value={local.id}>
                  {local.rotulo}
                </option>
              ))}
            </select>
          )}
        </div>
      )}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <Botao
        tipo="submit"
        desabilitado={!desafioEscolhido || !localId || enviando}
        onClick={aoEnviar}
      >
        Abrir série
      </Botao>
    </section>
  );
}

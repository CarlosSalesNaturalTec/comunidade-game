import type { DadosDaCarta } from "comum/react";
import type { ApoiadorPublico, MestrePublico } from "../api/leituras";

// Da resposta pública para as variantes **Mestre** e **Apoiador** da carta do
// documento 11 §8.2. Nenhuma das duas tem campo de valor em reais nem de
// contato de Guerreiro(a): é por não existir que nenhuma tela os põe lá
// (`RN-03-18`, `RN-03-26`).

/** A leitura como ela chega. Cada campo é opcional **de propósito**: quem
 * decide se a carta se apresenta é `cartaEstaCompleta`, e para decidir ela
 * precisa poder receber `undefined` (documento 11 §8.2). */
export type LeituraDoMestre = Partial<MestrePublico>;
export type LeituraDoApoiador = Partial<ApoiadorPublico>;

export function cartaDoMestre(mestre: LeituraDoMestre): DadosDaCarta {
  return {
    variante: "mestre",
    avatar: mestre.avatar,
    identificacao: mestre.identificacao,
    areasDeHabilidade: mestre.areas_de_habilidade,
    artefatos: mestre.artefatos,
    trilhasDeAutoria: mestre.trilhas_de_autoria?.map((trilha) => trilha.nome),
    absorcoes: mestre.absorcoes,
  };
}

export function cartaDoApoiador(apoiador: LeituraDoApoiador): DadosDaCarta {
  return {
    variante: "apoiador",
    avatar: apoiador.avatar,
    identificacao: apoiador.identificacao,
    totalEmMoedas: apoiador.total_em_moedas,
    avatarPadrao: apoiador.avatar_padrao,
    nivelDeSustento: apoiador.nivel_de_sustento,
    nomeDoNivel: apoiador.nome_do_nivel,
    selos: apoiador.selos?.map((selo) => selo.nome),
    desafiosPropostos: apoiador.desafios_propostos?.map((desafio) => ({
      trilha: desafio.trilha,
      periodoInicio: desafio.periodo_inicio,
      periodoFim: desafio.periodo_fim,
      concluiram: desafio.concluiram,
      direcionado: desafio.direcionado,
    })),
    artefatos: apoiador.artefatos,
  };
}

import { Cabecalho, Moldura } from "comum/react";

interface Props {
  aoVoltar: () => void;
}

interface DadoColetado {
  dado: string;
  finalidade: string;
  prazo: string;
  quemAcessa: string;
}

// Transcrição do PRD-04 §11, em linguagem de criança — a mesma tabela do
// documento-fonte, sem número nem regra nova (`RF-04-26`, `RN-04-06`,
// `RN-04-08`, `RN-04-09`, `RN-04-14`).
const DADOS_COLETADOS: DadoColetado[] = [
  {
    dado: "Fotografia captada",
    finalidade: "gerar o descritor facial no próprio aparelho",
    prazo: "apagada assim que o descritor é gerado — nunca sai do aparelho",
    quemAcessa: "ninguém: ela não viaja pela rede nem fica guardada",
  },
  {
    dado: "Descritor facial (o \"template\")",
    finalidade: "confirmar quem é você nos próximos encontros",
    prazo:
      "enquanto você participar, mais 30 dias — ou só 5 dias, se você pedir para apagar antes",
    quemAcessa: "ninguém vê: só a comparação interna confere",
  },
  {
    dado: "Nome",
    finalidade: "identificação para a gestão",
    prazo: "enquanto você participar",
    quemAcessa: "a gestão e seu responsável",
  },
  {
    dado: "Nick e forma de tratamento",
    finalidade: "sua identidade pública na plataforma",
    prazo: "enquanto você participar",
    quemAcessa: "qualquer visitante",
  },
  {
    dado: "Data de nascimento",
    finalidade: "saber sua faixa etária e o nível das atividades",
    prazo: "enquanto você participar",
    quemAcessa: "a gestão e seu responsável",
  },
  {
    dado: "Características do avatar",
    finalidade: "montar o seu avatar",
    prazo: "enquanto você participar",
    quemAcessa: "qualquer visitante",
  },
  {
    dado: "Áudio ou texto da conversa de cadastro",
    finalidade: "conduzir o cadastro",
    prazo: "descartado assim que o cadastro termina",
    quemAcessa: "ninguém, depois do atendimento",
  },
  {
    dado: "Foto ou áudio da produção da missão",
    finalidade: "ler o que a equipe produziu e dar um retorno",
    prazo: "descartados na leitura — fica só a transcrição e o retorno escrito",
    quemAcessa: "a gestão e o Mestre da turma",
  },
  {
    dado: "Áudio da pergunta ao assistente",
    finalidade: "gerar a transcrição da pergunta",
    prazo: "descartado assim que vira texto",
    quemAcessa: "ninguém: não fica guardado",
  },
  {
    dado: "Transcrição da conversa com o assistente",
    finalidade: "melhorar o material e conferir como a IA respondeu",
    prazo: "enquanto você participar",
    quemAcessa: "a gestão e o Mestre da trilha",
  },
  {
    dado: "Presença nos encontros",
    finalidade: "registrar que você participou",
    prazo: "enquanto você participar",
    quemAcessa: "a gestão e seu responsável",
  },
];

// Tela interna da própria aplicação, sem chamada ao núcleo — precisa abrir
// mesmo com a rede fora (design — decisão 10). Alcançável do aviso da tela
// inicial e do aviso da tela de captura.
export function AreaDetalhadaDeDireitos({ aoVoltar }: Props) {
  return (
    <Moldura>
      <Cabecalho
        titulo="O que a gente guarda sobre você"
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      <p>
        Aqui vai, em detalhe, tudo que a Comunidade Game coleta neste aparelho: para que serve,
        por quanto tempo fica guardado e quem pode ver.
      </p>
      <ul aria-label="Dados coletados">
        {DADOS_COLETADOS.map((item) => (
          <li key={item.dado}>
            <p>
              <strong>{item.dado}</strong>
            </p>
            <p>Para que serve: {item.finalidade}.</p>
            <p>Por quanto tempo fica: {item.prazo}.</p>
            <p>Quem acessa: {item.quemAcessa}.</p>
          </li>
        ))}
      </ul>

      <h3>Sua foto</h3>
      <p>
        A fotografia é apagada assim que o descritor é gerado, e nunca sai deste aparelho. Sua
        imagem nunca é mostrada a ninguém: ela não vira seu avatar, não aparece na vitrine, não
        entra em nenhum ranking e nenhum outro Guerreiro ou Guerreira a vê.
      </p>

      <h3>Se você não quiser usar a câmera</h3>
      <p>
        Sem problema nenhum — recusar a biometria não te tira de nada. Você entra do mesmo jeito
        dizendo seu nick, com um Mestre ou Admin confirmando quem você é.
      </p>

      <h3>Quer pedir para ver, corrigir ou apagar seus dados?</h3>
      <p>
        Esse pedido é feito pelo seu responsável, na App 07, e a resposta chega em até 7 dias.
        Esta aplicação aqui não recebe nem responde esse tipo de pedido.
      </p>
    </Moldura>
  );
}

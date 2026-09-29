import { Moldura, Tabela } from "comum/react";

// A área detalhada de coleta (`RF-03-52`, `RF-03-53`, `RN-03-23`). É texto
// fixo da aplicação, em linguagem simples, derivado da tabela do PRD-03 §11
// e do documento 03 §§12.1 e 12.2 — sem número que esses documentos não
// tragam (design — decisão 8). Não é editável pelo Admin.

interface DadoDaVitrine {
  dado: string;
  deQuem: string;
  paraQue: string;
  prazo: string;
}

const DADOS_DA_VITRINE: DadoDaVitrine[] = [
  {
    dado: "Nada do visitante",
    deQuem: "—",
    paraQue: "—",
    prazo: "—",
  },
  {
    dado: "Pedido para ser Mestre ou Apoiador",
    deQuem: "Quem preenche o formulário de participação",
    paraQue: "Avaliar quem pede para entrar",
    prazo: "Até a resposta e o registro dela",
  },
  {
    dado: "Pedido do conjunto de dados",
    deQuem: "Quem preenche o formulário de dados",
    paraQue: "Avaliar o pedido e registrar a entrega",
    prazo: "Para sempre, como prova do que foi entregue",
  },
  {
    dado: "Pedido de chave da API",
    deQuem: "Quem quer construir sobre a plataforma",
    paraQue: "Avaliar quem vai construir sobre a API",
    prazo: "Enquanto a chave existir",
  },
  {
    dado: "Conversa com o assistente do Desenvolvedor",
    deQuem: "Quem conversa com o assistente",
    paraQue: "Responder a pergunta do momento",
    prazo: "Não é guardada: some ao fechar a página",
  },
  {
    dado: "Avatar, nick e desempenho mostrados na vitrine",
    deQuem: "Guerreiro(a) cujo responsável autorizou",
    paraQue: "Reconhecer o Guerreiro(a) em público",
    prazo: "Enquanto a autorização durar",
  },
  {
    dado: "Séries do território mostradas na vitrine",
    deQuem: "Do lugar, agregadas até o bairro, sem código de quem coletou",
    paraQue: "Ser um bem público e evidência sobre o lugar",
    prazo: "Para sempre, agregadas",
  },
];

interface PrazoDeGuarda {
  dado: string;
  prazo: string;
}

const PRAZOS_DA_PLATAFORMA: PrazoDeGuarda[] = [
  {
    dado: "Conversa respondida nas aplicações do Guerreiro(a)",
    prazo: "7 dias ligada ao Guerreiro(a); depois ficam só a disciplina e a data",
  },
  { dado: "Conversa recusada pelos filtros", prazo: "Até o fim do ciclo, só a gestão vê" },
  {
    dado: "Sugestão não adotada",
    prazo: "90 dias depois da resposta a quem sugeriu",
  },
  {
    dado: "Sugestão adotada",
    prazo: "Para sempre, com o crédito a quem sugeriu",
  },
  {
    dado: "Foto da produção do Guerreiro(a)",
    prazo: "Descartada na leitura; ficam a transcrição e a devolutiva",
  },
  {
    dado: "Áudio de qualquer origem",
    prazo: "Descartado na transcrição; a fala é transcrita no aparelho",
  },
  {
    dado: "Contexto de personalização da sessão",
    prazo: "Descartado ao fim da sessão; nada é adivinhado nem guardado",
  },
  {
    dado: "Motivo de uma ocorrência de conduta",
    prazo: "Até o fim do ciclo em que ocorreu; fica só o lançamento",
  },
  {
    dado: "Modelo do rosto (reconhecimento facial)",
    prazo:
      "30 dias depois do fim do vínculo, com aviso ao responsável; 5 dias se o responsável recusar ou pedir a exclusão",
  },
  {
    dado: "Contadores de custo e demanda de IA",
    prazo: "Para sempre, sem nenhum dado pessoal",
  },
];

export function AreaDetalhada() {
  return (
    <Moldura>
      <div className="cg-vitrine cg-area-detalhada">
        <h2>O que a plataforma coleta</h2>

        <section>
          <h3>A vitrine não coleta nada de quem visita</h3>
          <p>
            Sem login, sem cadastro, sem cookie de rastreio e sem perfil do visitante. Também
            não guardamos favoritos, preferências nem histórico de navegação: se você
            recarregar a página, ela volta a ser como na primeira visita.
          </p>
        </section>

        <section>
          <h3>O que a vitrine mostra e o que os formulários guardam</h3>
          <Tabela
            legenda="Dados ligados à vitrine"
            colunas={[
              {
                chave: "dado",
                rotulo: "Dado",
                cabecalhoDeLinha: true,
                renderizar: (linha: DadoDaVitrine) => linha.dado,
              },
              { chave: "de-quem", rotulo: "De quem", renderizar: (linha) => linha.deQuem },
              { chave: "para-que", rotulo: "Para quê", renderizar: (linha) => linha.paraQue },
              {
                chave: "prazo",
                rotulo: "Por quanto tempo",
                renderizar: (linha) => linha.prazo,
              },
            ]}
            linhas={DADOS_DA_VITRINE}
            chaveDaLinha={(linha) => linha.dado}
          />
        </section>

        <section>
          <h3>O dado do território</h3>
          <p>
            O valor medido, o local e a data são dado do lugar, e saem agregados até o bairro.
            Quem coletou é o único dado pessoal do registro: fica guardado com o consentimento
            do responsável e nunca aparece junto da medição. Se o consentimento é revogado, o
            vínculo se rompe e a medição continua na série, sem ligação com pessoa alguma.
          </p>
        </section>

        <section>
          <h3>Outros prazos de guarda na plataforma</h3>
          <Tabela
            legenda="Prazos de guarda dos dados das aplicações"
            colunas={[
              {
                chave: "dado",
                rotulo: "Dado",
                cabecalhoDeLinha: true,
                renderizar: (linha: PrazoDeGuarda) => linha.dado,
              },
              {
                chave: "prazo",
                rotulo: "Por quanto tempo",
                renderizar: (linha) => linha.prazo,
              },
            ]}
            linhas={PRAZOS_DA_PLATAFORMA}
            chaveDaLinha={(linha) => linha.dado}
          />
        </section>
      </div>
    </Moldura>
  );
}

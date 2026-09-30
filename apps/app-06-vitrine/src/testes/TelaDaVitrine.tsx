import { Cabecalho, FundoDeComunidade, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { PaginaDoApoiador } from "../adultos/PaginaDoApoiador";
import { PaginaDoMestre } from "../adultos/PaginaDoMestre";
import { SecaoDeApoiadores } from "../adultos/SecaoDeApoiadores";
import { SecaoDeMestres } from "../adultos/SecaoDeMestres";
import type { ChaveDeSecaoInstitucional } from "../api/leituras";
import { AreaDetalhada } from "../coleta/AreaDetalhada";
import { AvisoDeColeta } from "../coleta/AvisoDeColeta";
import { PortaDoConvite } from "../convite/PortaDoConvite";
import { ApresentacaoDaUrl } from "../desenvolvedor/ApresentacaoDaUrl";
import { AreaDoDesenvolvedor } from "../desenvolvedor/AreaDoDesenvolvedor";
import { SecaoDoDesenvolvedor } from "../desenvolvedor/SecaoDoDesenvolvedor";
import { DialogoDeEntrada } from "../entrada/DialogoDeEntrada";
import { FormularioDeDados } from "../formularios/FormularioDeDados";
import { FormularioDeParticipacao } from "../formularios/FormularioDeParticipacao";
import { SecaoDeSolicitacaoDeDados } from "../formularios/SecaoDeSolicitacaoDeDados";
import { PaginaDoGuerreiro } from "../guerreiros/PaginaDoGuerreiro";
import { SecaoDeGuerreiros } from "../guerreiros/SecaoDeGuerreiros";
import { RolagemAteAAncora } from "../institucional/RolagemAteAAncora";
import {
  ApresentacaoDaSecao,
  NecessidadesEmAberto,
} from "../institucional/SecoesInstitucionais";
import { useConteudoInstitucional } from "../institucional/useConteudoInstitucional";
import {
  CAMINHO_DA_APRESENTACAO_DA_URL,
  CAMINHO_DA_AREA_DETALHADA,
  CAMINHO_DA_AREA_DO_DESENVOLVEDOR,
  CAMINHO_DA_PARTICIPACAO,
  CAMINHO_DA_SOLICITACAO_DE_DADOS,
  CAMINHO_DO_CONVITE,
} from "../navegacao/caminhos";
import {
  apoiadorDoCaminho,
  comunidadeDoCaminho,
  mestreDoCaminho,
  nickDoCaminho,
  RECORTES,
  recorteDoCaminho,
} from "../navegacao/recortes";
import { SecaoDePoderes } from "../poderes/SecaoDePoderes";
import { SecaoDoPortfolio } from "../portfolio/SecaoDoPortfolio";
import { SecaoDoRanking } from "../ranking/SecaoDoRanking";
import { BlocoDoGestor } from "../territorio/BlocoDoGestor";
import { PaginaDaComunidade } from "../territorio/PaginaDaComunidade";
import { SecaoDaCobertura } from "../territorio/SecaoDaCobertura";
import { SecaoDeComunidades } from "../territorio/SecaoDeComunidades";

/**
 * **Só para teste.** Não entra em nenhum pacote publicado.
 *
 * Monta, no jsdom, a mesma composição de tela que as páginas de `src/pages/`
 * montam no build, e navega entre elas **no cliente**. Existe porque a
 * produção passou a navegar por carga de documento, que o jsdom não executa:
 * sem isso, os 118 casos da App 06 não teriam onde afirmar que acionar um card
 * leva à página daquele card.
 *
 * O que cada caso afirma continua sendo comportamento que a produção tem — os
 * componentes são os mesmos, montados na mesma ordem. O que esta composição
 * substitui é só a carga de documento.
 *
 * **Ela pode desviar das páginas reais**, e é por isso que o teste da saída do
 * build (`saidaDoBuild.test.ts`) confere título e seções rota a rota sobre o
 * `dist/`: um desvio quebra lá (design — decisão 7).
 */

/** O institucional lido no cliente. Na produção o Astro busca no build e
 * entrega o dado pronto a `ApresentacaoDaSecao`; aqui a leitura é a mesma que
 * a `PortaDoConvite` já faz em produção. */
function SecaoInstitucional({
  secao,
  nome,
}: {
  secao: ChaveDeSecaoInstitucional;
  nome: string;
}) {
  const estado = useConteudoInstitucional(secao);
  if (estado.situacao !== "pronta") return null;
  return <ApresentacaoDaSecao dado={estado.dado} nome={nome} />;
}

function Secao({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <section>
      <h2>{titulo}</h2>
      {children}
    </section>
  );
}

function SecoesDoRecorte({
  caminho,
  irPara,
}: {
  caminho: string;
  irPara: (destino: string) => void;
}) {
  const recorte = recorteDoCaminho(caminho);

  if (recorte.chave === "sociedade-civil") {
    return (
      <>
        <Secao titulo="Quem somos">
          <SecaoInstitucional secao="quem-somos" nome="Quem somos" />
          <RolagemAteAAncora />
        </Secao>
        <Secao titulo="Guerreiros e Guerreiras">
          <SecaoDeGuerreiros irPara={irPara} />
        </Secao>
        <Secao titulo="Portfólio de criações originais">
          <SecaoDoPortfolio />
        </Secao>
        <Secao titulo="Ranking">
          <SecaoDoRanking />
        </Secao>
        <Secao titulo="Poderes">
          <SecaoDePoderes irPara={irPara} />
        </Secao>
        <Secao titulo="Mestres">
          <SecaoDeMestres irPara={irPara} />
        </Secao>
        <Secao titulo="Apoiadores">
          <SecaoDeApoiadores irPara={irPara} />
        </Secao>
        <Secao titulo="Comunidades Virtuais">
          <SecaoDeComunidades irPara={irPara} />
        </Secao>
        <Secao titulo="Construir sobre a API">
          <SecaoDoDesenvolvedor irPara={irPara} />
        </Secao>
        <Secao titulo="Como apoiar">
          <SecaoInstitucional secao="como-apoiar" nome="Como apoiar" />
          <NecessidadesEmAberto />
        </Secao>
        <Secao titulo="Contatos">
          <SecaoInstitucional secao="contatos" nome="Contatos" />
        </Secao>
      </>
    );
  }

  return (
    <>
      {recorte.chave === "gestores-publicos" && (
        <Secao titulo="Para que a plataforma serve ao município">
          <BlocoDoGestor />
        </Secao>
      )}
      <Secao titulo="Séries do território e metodologia">
        <SecaoDeComunidades irPara={irPara} />
      </Secao>
      <Secao titulo="Cobertura da Agenda 2030">
        <SecaoDaCobertura />
      </Secao>
      <Secao titulo="Solicitação do conjunto de dados">
        <SecaoDeSolicitacaoDeDados irPara={irPara} />
      </Secao>
      <Secao titulo="Contatos">
        <SecaoInstitucional secao="contatos" nome="Contatos" />
      </Secao>
    </>
  );
}

export function TelaDaVitrine() {
  const [caminho, definirCaminho] = useState(() => window.location.pathname);
  const [entradaAberta, definirEntradaAberta] = useState(false);
  const empilhados = useState({ total: 0 })[0];

  useEffect(() => {
    function aoVoltar() {
      if (empilhados.total > 0) empilhados.total -= 1;
      definirCaminho(window.location.pathname);
    }
    window.addEventListener("popstate", aoVoltar);
    return () => window.removeEventListener("popstate", aoVoltar);
  }, [empilhados]);

  const irPara = useCallback(
    (destino: string) => {
      if (destino === window.location.pathname) return;
      window.history.pushState(null, "", destino);
      empilhados.total += 1;
      definirCaminho(destino);
    },
    [empilhados],
  );

  const voltar = useCallback(() => {
    if (empilhados.total > 0) {
      window.history.back();
      return;
    }
    window.history.pushState(null, "", "/");
    definirCaminho("/");
  }, [empilhados]);

  const nick = nickDoCaminho(caminho);
  const comunidadeId = comunidadeDoCaminho(caminho);
  const mestreId = mestreDoCaminho(caminho);
  const apoiadorId = apoiadorDoCaminho(caminho);
  const ehRecorte = RECORTES.some((recorte) => recorte.caminho === caminho);

  function conteudo() {
    if (caminho === CAMINHO_DA_PARTICIPACAO)
      return <FormularioDeParticipacao irPara={irPara} />;
    if (caminho === CAMINHO_DA_SOLICITACAO_DE_DADOS)
      return <FormularioDeDados irPara={irPara} />;
    if (caminho === CAMINHO_DO_CONVITE)
      return <PortaDoConvite irPara={irPara} voltar={voltar} />;
    if (caminho === CAMINHO_DA_AREA_DETALHADA) return <AreaDetalhada />;
    if (caminho === CAMINHO_DA_AREA_DO_DESENVOLVEDOR)
      return <AreaDoDesenvolvedor irPara={irPara} />;
    if (caminho === CAMINHO_DA_APRESENTACAO_DA_URL)
      return <ApresentacaoDaUrl irPara={irPara} />;
    if (nick !== null) return <PaginaDoGuerreiro nick={nick} irPara={irPara} />;
    if (comunidadeId !== null)
      return <PaginaDaComunidade comunidadeId={comunidadeId} irPara={irPara} />;
    if (mestreId !== null) return <PaginaDoMestre mestreId={mestreId} irPara={irPara} />;
    if (apoiadorId !== null)
      return <PaginaDoApoiador apoiadorId={apoiadorId} irPara={irPara} />;
    return <SecoesDoRecorte caminho={caminho} irPara={irPara} />;
  }

  return (
    // A moldura da Arena, como em `Vitrine.astro`: sem ela aqui, a composição
    // de teste desviaria do layout — e é o teste da saída do build que
    // acusaria (design — decisão 6).
    <FundoDeComunidade imagem={null}>
      <Cabecalho
        titulo="Comunidade Game"
        subtitulo="A vitrine pública do projeto — aberta, sem cadastro e sem login."
        acao={{ rotulo: "Entrar", aoAcionar: () => definirEntradaAberta(true) }}
      />
      <nav className="cg-recortes" aria-label="Recortes de leitura">
        {RECORTES.map((recorte) => (
          <button
            key={recorte.chave}
            type="button"
            className="cg-recortes__item"
            aria-current={ehRecorte && recorte.caminho === caminho ? "true" : undefined}
            onClick={() => irPara(recorte.caminho)}
          >
            {recorte.rotulo}
          </button>
        ))}
      </nav>
      <Moldura>
        <div className="cg-vitrine">{conteudo()}</div>
      </Moldura>
      <AvisoDeColeta irPara={irPara} />
      <DialogoDeEntrada aberto={entradaAberta} aoFechar={() => definirEntradaAberta(false)} />
    </FundoDeComunidade>
  );
}

export default TelaDaVitrine;

import { Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { AreaDetalhada } from "./coleta/AreaDetalhada";
import { AvisoDeColeta } from "./coleta/AvisoDeColeta";
import { PortaDoConvite } from "./convite/PortaDoConvite";
import { DialogoDeEntrada } from "./entrada/DialogoDeEntrada";
import { FormularioDeDados } from "./formularios/FormularioDeDados";
import { FormularioDeParticipacao } from "./formularios/FormularioDeParticipacao";
import { PaginaDoGuerreiro } from "./guerreiros/PaginaDoGuerreiro";
import {
  CAMINHO_DA_AREA_DETALHADA,
  CAMINHO_DA_PARTICIPACAO,
  CAMINHO_DA_SOLICITACAO_DE_DADOS,
  CAMINHO_DO_CONVITE,
} from "./navegacao/caminhos";
import { NavegacaoDeRecortes } from "./navegacao/NavegacaoDeRecortes";
import { comunidadeDoCaminho, nickDoCaminho, recorteDoCaminho } from "./navegacao/recortes";
import { useNavegacao } from "./navegacao/useNavegacao";
import { TelaDoRecorte } from "./recortes/TelaDoRecorte";
import { PaginaDaComunidade } from "./territorio/PaginaDaComunidade";

// A vitrine não monta `ProvedorDeSessao` nem `ProvedorDeNarracao`: o primeiro
// guarda sessão e o segundo guarda a preferência do aparelho, e aqui nada do
// visitante é guardado (`RF-03-51`, `RN-03-01`, `RN-03-22`). Sem provedor, a
// camada de narração fica inerte por construção.
export default function App() {
  const { caminho, irPara, voltar } = useNavegacao();
  const [entradaAberta, definirEntradaAberta] = useState(false);
  const recorte = recorteDoCaminho(caminho);
  const nick = nickDoCaminho(caminho);
  const comunidadeId = comunidadeDoCaminho(caminho);

  return (
    <>
      {/* O "Entrar" fica no cabeçalho, presente em toda tela pública
          (`RF-03-58`). */}
      <Cabecalho
        titulo="Comunidade Game"
        subtitulo="A vitrine pública do projeto — aberta, sem cadastro e sem login."
        acao={{ rotulo: "Entrar", aoAcionar: () => definirEntradaAberta(true) }}
      />
      <NavegacaoDeRecortes recorteAtual={recorte.chave} aoSelecionarRecorte={irPara} />
      {/* A página individual tem endereço próprio, compartilhável e
          alcançável direto (`RF-03-03`); todo o resto é o recorte. */}
      {caminho === CAMINHO_DA_PARTICIPACAO ? (
        <FormularioDeParticipacao irPara={irPara} />
      ) : caminho === CAMINHO_DA_SOLICITACAO_DE_DADOS ? (
        <FormularioDeDados irPara={irPara} />
      ) : caminho === CAMINHO_DO_CONVITE ? (
        <PortaDoConvite irPara={irPara} voltar={voltar} />
      ) : caminho === CAMINHO_DA_AREA_DETALHADA ? (
        <AreaDetalhada />
      ) : nick !== null ? (
        <Moldura>
          <div className="cg-vitrine">
            <PaginaDoGuerreiro nick={nick} irPara={irPara} />
          </div>
        </Moldura>
      ) : comunidadeId !== null ? (
        <Moldura>
          <div className="cg-vitrine">
            <PaginaDaComunidade comunidadeId={comunidadeId} irPara={irPara} />
          </div>
        </Moldura>
      ) : (
        <TelaDoRecorte recorte={recorte} irPara={irPara} />
      )}
      {/* O aviso de coleta vale para toda tela, e por isso mora aqui, fora do
          recorte (`RN-03-23`). */}
      <AvisoDeColeta irPara={irPara} />
      <DialogoDeEntrada aberto={entradaAberta} aoFechar={() => definirEntradaAberta(false)} />
    </>
  );
}
